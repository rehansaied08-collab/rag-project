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
    return {"status": "ok"}  

@app.get("/test-gemini")
def test_gemini():
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.5-flash")


        outline_prompt = "Create a 3-point outline explaining what a large language model is."

        outline_response = model.generate_content(outline_prompt)
        outline_text = outline_response.text

        if not outline_text:
            raise ValueError("Step 1 failed: No outline generated.")

      
        expansion_prompt = f"""
        Using the following outline:

        {outline_text}

        Write one clear paragraph expanding on these points.
        """

        final_response = model.generate_content(expansion_prompt)
        final_text = final_response.text

        if not final_text:
            raise ValueError("Step 2 failed: No final response generated.")

        return {"response": final_text}

    except Exception as e:
        return {"error": "Multi-step Gemini call failed: " + str(e)}