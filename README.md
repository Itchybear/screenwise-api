# Screenwise API

The Screenwise API is a small backend project that acts as an AI-powered interview screener.  
You send it candidate answers, and it gives back a score (1–5), a one-line summary, and one suggestion to improve the answer. It can also compare multiple candidates and return them in ranked order.

No frontend, no heavy setup, just clean and simple APIs that can plug into any UI or hiring workflow.

## What the API can do

### `/evaluate-answer`
Takes one answer and returns:
- A score from 1 to 5
- A quick summary of what the answer conveys
- One improvement suggestion

### `/rank-candidates`
Takes multiple answers and returns a list sorted by score (best -> worst), along with summaries and improvement notes for each.

## How it's designed

The backend is built with **FastAPI** because it’s fast to develop, easy to maintain, and returns clean JSON by default.  
The evaluation function was originally structured to call an LLM (e.g., OpenAI / Claude / LLaMA), but for demo and testing without API tokens, a fallback scoring algorithm is used. It looks for relevant behaviours such as teamwork, communication, and conflict resolution, and generates a realistic score and feedback.

If an LLM API is plugged in later, nothing else in the backend needs to change, just the evaluator function.

## Tech used
- Python
- FastAPI
- Uvicorn
- Pydantic
- OpenAI integration

## How to run the project

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

http://127.0.0.1:8000 -> server running

http://127.0.0.1:8000/docs -> interactive API testing
