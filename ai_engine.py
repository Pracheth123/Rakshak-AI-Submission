import json
from groq import AsyncGroq
from config import settings

class ScamProtector:
    def __init__(self):
        print("🧠 Actual AI Mode Enabled (Groq LLM Engine)")
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)

    async def analyze(self, text: str):
        # 1. LOWERED THE LIMIT TO 5 CHARACTERS
        if not text or len(text.strip()) < 5:
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
                model="llama-3.1-8b-instant", 
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}, 
                temperature=0.1, 
            )
            
            raw_response = completion.choices[0].message.content.strip()
            result = json.loads(raw_response)
            
            # 2. X-RAY VISION: Print exactly what the AI decided to the terminal!
            print(f"🤖 AI Decision for '{text}': {result.get('is_threat')} | Label: {result.get('label')}")
            
            # 3. Handle boolean True or string "true" safely
            is_threat = result.get("is_threat")
            if is_threat is True or str(is_threat).lower() == "true":
                return result
                
            return None
            
        except Exception as e:
            print(f"❌ LLM Error: {e}") 
            return None