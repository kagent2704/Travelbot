import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))  # Load from app/

# API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Ensure API keys are loaded
if not GEMINI_API_KEY:
    raise ValueError("❌ Gemini API key is missing. Set it in your .env file.")
