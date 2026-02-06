import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    # --- ARCHITECTURE FLAGS ---
    # Set to False for Hackathon Demo (Deepgram + Regex)
    # Set to True later if you get AWS credits (AWS Transcribe + Bedrock)
    USE_AWS = False  

    # --- API KEYS ---
    # Current: Free Tier Key for Deepgram
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    
    # Future: AWS Credentials (will load from .env when needed)
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Create a global settings object to import elsewhere
settings = Config()