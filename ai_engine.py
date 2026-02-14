import json
from groq import AsyncGroq
from config import settings # Let's go back to using your config file securely!

class ScamProtector:
    def __init__(self):
        print("🧠 Actual AI Mode Enabled (Groq LLM Engine)")
        # Make sure your GROQ_API_KEY is in your .env file!
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)

    async def analyze(self, text: str):
        if not text or len(text.strip()) < 10:
            return None

        prompt = f"""
        Analyze this live phone call transcript: "{text}"
        Is it a scam, suspicious, or safe?
        Output ONLY valid JSON:
        {{
            "is_threat": true or false,
            "label": "Safe" or "Suspicious" or "CRITICAL THREAT",
            "score": integer (0-100),
            "confidence": integer (0-100),
            "color": "bg-emerald-500" or "bg-orange-500" or "bg-red-500",
            "reason": "Short explanation",
            "triggers": ["extract", "exact", "words", "from", "text"] 
        }}
        """
        
        try:
            completion = await self.client.chat.completions.create(
                model="llama-3.1-8b-instant", # <-- THIS IS THE NEW SUPPORTED MODEL
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}, # Forces perfect JSON output
                temperature=0.1, 
            )
            
            raw_response = completion.choices[0].message.content.strip()
            result = json.loads(raw_response)
            
            if result.get("is_threat") is True or result.get("is_threat") == "true" or result.get("is_threat") == "True":
                return result
                
            return None
            
        except Exception as e:
            print(f"LLM Error: {e}") 
            return None