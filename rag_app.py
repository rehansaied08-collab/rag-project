import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")
genai.configure(api_key=api_key)

app = FastAPI()

# ---------------------------
# Models
# ---------------------------
class QueryRequest(BaseModel):
    question: str

# ---------------------------
# Validation functions
# ---------------------------
def validate_user_input(text: str):
    if text is None or text.strip() == "":
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    if len(text) < 5:
        raise HTTPException(status_code=400, detail="Question is too short")
    if len(text) > 500:
        raise HTTPException(status_code=400, detail="Question is too long")

def validate_model_output(text: str):
    if text is None or text.strip() == "":
        raise HTTPException(status_code=500, detail="AI returned an empty response")
    if len(text) < 10:
        raise HTTPException(status_code=500, detail="AI response is too short")

# ---------------------------
# Second AI model review
# ---------------------------
def review_model_output(original_answer: str):
    review_prompt = f"""
You are reviewing an AI-generated response.

Your job:
- If the response is unclear, incomplete, or poorly written, improve it.
- If the response is already good, return it unchanged.

AI response to review:
{original_answer}
"""
    review_model = genai.GenerativeModel("gemini-pro")
    review_response = review_model.generate_content(review_prompt)
    return review_response.text

# ---------------------------
# Endpoints
# ---------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/test-gemini")
def test_gemini():
    try:
        model = genai.GenerativeModel("gemini-pro")
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

@app.post("/query")
def query_ai(request: QueryRequest):
    validate_user_input(request.question)

    try:
        # First AI model
        primary_model = genai.GenerativeModel("gemini-pro")
        primary_response = primary_model.generate_content(request.question)
        raw_answer = primary_response.text

        validate_model_output(raw_answer)

        # Second AI model review
        reviewed_answer = review_model_output(raw_answer)

        return {
            "question": request.question,
            "answer": reviewed_answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI call failed: {str(e)}")