import json
import asyncio
import boto3
import re
import os

class ScamProtector:
    def __init__(self):
        # Initialize AWS Bedrock Runtime Client
        # It automatically picks up the AWS keys from your .env file
        region = os.getenv("AWS_REGION", "ap-south-1")
        self.client = boto3.client('bedrock-runtime', region_name=region)

    async def analyze(self, text: str):
        if not text or len(text.strip()) < 5:
            return None

        # =========================================================
        # NEW: ANTI-HALLUCINATION PROMPT (Few-Shot Calibration)
        # =========================================================
        prompt = f"""
        You are an expert cybersecurity AI. Analyze this live phone call transcript: "{text}"
        
        Task: Categorize the text strictly into one of three labels. Do not hallucinate threats in normal conversations.
        
        Definitions:
        1. "Safe": Everyday casual conversations, work updates, talking about traffic, weather, or friends. (e.g., "Main aaj late aunga, traffic bahut hai.")
        2. "Suspicious": Asking for OTPs, unknown bank verification calls, unexpected urgency.
        3. "CRITICAL THREAT": "Digital Arrest" scams, impersonating Police/CBI/FedEx, threatening jail time, forcing the user not to disconnect or talk to family.

        Output ONLY valid JSON. No markdown tags, no conversational text.
        {{
            "is_threat": true or false,
            "label": "Safe" or "Suspicious" or "CRITICAL THREAT",
            "action": "none" or "silent_guardian",
            "score": integer (0-20 for Safe, 50-80 for Suspicious, 90-100 for CRITICAL),
            "confidence": integer (0-100),
            "color": "bg-emerald-500" if Safe, "bg-orange-500" if Suspicious, "bg-rose-500" if CRITICAL,
            "reason": "1-sentence explanation of why",
            "triggers": ["extract", "suspicious", "words"] (Leave empty if Safe)
        }}
        """
        
        messages = [{"role": "user", "content": [{"text": prompt}]}]

        def invoke():
            # Temperature set to 0.0 forces purely logical, non-creative responses
            return self.client.converse(
                modelId="meta.llama3-8b-instruct-v1:0",
                messages=messages,
                inferenceConfig={"temperature": 0.0, "maxTokens": 512} 
            )

        try:
            # Run the Bedrock call in a background thread so it doesn't block the WebSocket audio stream
            response = await asyncio.to_thread(invoke)
            raw_text = response['output']['message']['content'][0]['text']
            
            # Clean any stray markdown formatting the LLM might output (e.g., ```json ... ```)
            clean_json_string = re.sub(r'```json\n|\n```|```', '', raw_text).strip()
            result = json.loads(clean_json_string)
            
            return result
            
        except Exception as e:
            print(f"❌ AWS Bedrock Error: {e}") 
            return None