import re
from config import settings

class ScamProtector:
    def __init__(self):
        # Flexible Architecture: Designed to swap between Regex and AWS Bedrock
        if settings.USE_AWS:
            print("⚠️ AWS Mode Enabled")
        else:
            print("✅ Local Mode Enabled")

    def analyze(self, text: str):
        patterns = {
            "financial": [r"card number", r"cvv", r"expiry date", r"credit card", r"debit card", r"bank account", r"payment"],
            "urgency": [r"immediately", r"urgent", r"block your card", r"suspended", r"expires soon", r"act now", r"police"],
            "sensitive": [r"otp", r"password", r"pin code", r"verification code"]
        }
        
        text_lower = text.lower()
        detected_cats = []
        
        for category, keywords in patterns.items():
            for k in keywords:
                if re.search(k, text_lower):
                    detected_cats.append(category)
                    break

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