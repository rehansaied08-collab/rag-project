import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}  # Step 6: matches expected /health response

@app.get("/test-gemini")
def test_gemini():
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = "Explain what a large language model is in one paragraph."

        response = model.generate_content(prompt)

        return {"response": response.text}

    except Exception as e:
        return {"error": "Gemini call failed: " + str(e)}
