import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Service Flags
    USE_AWS = False  # Set to True later when you get credits

    # Keys
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    
    # AWS Config
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

settings = Config()