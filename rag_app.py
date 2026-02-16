import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read the Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Fail clearly if missing
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

# Create FastAPI app
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "Server is running"}
