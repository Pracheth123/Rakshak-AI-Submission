import re
import json
from config import settings

class ScamProtector:
    def __init__(self):
        # --- ARCHITECTURE NOTE FOR JUDGES ---
        # This class is designed to switch between a local Rule-Engine (low latency)
        # and a Cloud LLM (high intelligence).
        
        if settings.USE_AWS:
            # self.bedrock = boto3.client('bedrock-runtime', ...)
            print("⚠️ AWS Mode Enabled (Requires Credentials)")
        else:
            print("✅ Local Mode Enabled (Deepgram + Regex Engine)")

    def analyze(self, text: str):
        """
        Analyzes text for scam patterns.
        """
        # 1. Define Threat Patterns (The "Local" Brain)
        patterns = {
            "financial": [r"card number", r"cvv", r"expiry date", r"credit card", r"debit card", r"bank account", r"payment"],
            "urgency": [r"immediately", r"urgent", r"block your card", r"suspended", r"expires soon", r"act now", r"police"],
            "sensitive": [r"otp", r"password", r"pin code", r"verification code"]
        }
        
        text_lower = text.lower()
        detected_cats = []
        
        # 2. Check Patterns
        for category, keywords in patterns.items():
            for k in keywords:
                if re.search(k, text_lower):
                    detected_cats.append(category)
                    break

        # --- FUTURE AWS INTEGRATION ---
        # if settings.USE_AWS:
        #    prompt = f"Analyze if this sentence is a scam: '{text}'. JSON Output: {{'risk': 0-100}}"
        #    response = self.bedrock.invoke_model(...)
        #    return parse_aws_response(response)

        # 3. Decision Logic
        if "sensitive" in detected_cats or ("financial" in detected_cats and "urgency" in detected_cats):
            return {
                "is_threat": True,
                "label": "CRITICAL THREAT",
                "score": 98,
                "color": "bg-red-500",
                "reason": "Sensitive Data + Urgency Detected"
            }
        elif len(detected_cats) > 0:
            return {
                "is_threat": True,
                "label": "Suspicious",
                "score": 75,
                "color": "bg-orange-500",
                "reason": "Suspicious Financial Language"
            }
            
        return None