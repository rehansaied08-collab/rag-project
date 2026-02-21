# RAG Project

This repository contains my Retrieval-Augmented Generation (RAG) project for the GenAI Secure Coding course.

This project will be built incrementally each week.



## Git Commands Used So Far

* git clone
* git status
* git add
* git commit
* git push



\## Week 4 Progress



\- Set up project structure

\- Created rag\_app.py with FastAPI

\- Installed dependencies from requirements.txt

\- Configured .env to securely store the Gemini API key

\- Verified server runs locally at /health

\- Did not implement Gemini logic yet



\## Week 5 — Gemini API Integration



\*\*/test-gemini endpoint\*\*  

This endpoint sends a hardcoded prompt to the Gemini model (`gemini-2.5-flash`) and returns the AI-generated response as JSON.  



\*\*Where the Gemini call lives\*\*  

All Gemini API logic is inside the `test\_gemini()` function in `rag\_app.py`. The API key is loaded from `.env` and never exposed to the client.  



\*\*What I learned\*\*  

\- How to initialize a Gemini model using the `google-generativeai` Python SDK  

\- How to send a prompt and extract the response  

\- Best practices for keeping API keys server-side  

\- How FastAPI endpoints return JSON responses  



## Week 6 — Multi-Step Execution

This week is  the Gemini endpoint to do two sequence AI calls.

Step 1: Generate an outline on a topic.
Step 2: Use that outline to generate a more expanded response.

The output of Step 1 is passed directly to  Step 2.
Only the final expanded result is returned to the client.

This shows a structured multi-step execution instead of a single prompt-response pattern.



