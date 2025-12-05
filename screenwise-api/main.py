from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Screenwise API - Mini AI Interview Screener (Fallback Only)")


# ---------- Models ----------

class EvaluateRequest(BaseModel):
    answer: str


class EvaluationResponse(BaseModel):
    score: int
    summary: str
    improvement: str


class RankRequest(BaseModel):
    answers: List[str]


class RankedCandidate(BaseModel):
    answer: str
    score: int
    summary: str
    improvement: str


# ---------- Fallback "AI" Evaluator (Rule-Based) ----------

def fallback_evaluate(answer: str) -> dict:
    """
    Simple rule-based evaluator to mimic AI behavior.
    Scores based on presence of keywords like:
    - teamwork
    - communication
    - problem-solving / conflict resolution
    """

    text = answer.lower()

    score = 1
    reasons = []

    # Heuristic scoring rules
    if any(w in text for w in ["team", "teamwork", "collaborate", "collaboration", "together"]):
        score += 1
        reasons.append("Mentions teamwork.")
    if any(w in text for w in ["communicate", "communication", "listening", "listen", "clarify"]):
        score += 1
        reasons.append("Mentions communication.")
    if any(w in text for w in ["resolve", "conflict", "problem", "issue", "solution", "solve"]):
        score += 1
        reasons.append("Mentions problem-solving or conflict resolution.")
    if len(answer.strip()) > 150:
        score += 1
        reasons.append("Provides a detailed and elaborate answer.")

    # Clamp score between 1 and 5
    if score < 1:
        score = 1
    if score > 5:
        score = 5

    if not reasons:
        summary = "Answer is vague and does not clearly show relevant skills."
        improvement = "Mention specific skills like teamwork, communication, and problem-solving with a real example."
    else:
        summary = " ".join(reasons)
        improvement = "Add a concrete example or situation to demonstrate these skills in practice."

    return {
        "score": score,
        "summary": summary,
        "improvement": improvement,
    }


# ---------- Wrapper (keeps LLM-style name for assignment) ----------

def evaluate_with_llm(answer: str) -> dict:
    """
    In a real deployment, this would call an LLM API (OpenAI, Claude, LLaMA, etc.).
    For this implementation (no quota / no billing), we use a local rule-based fallback.
    """
    return fallback_evaluate(answer)


# ---------- Routes ----------

@app.get("/")
def root():
    return {"message": "Mini AI Interview Screener is running (fallback mode)"}


@app.post("/evaluate-answer", response_model=EvaluationResponse)
def evaluate_answer(payload: EvaluateRequest):
    """
    Takes a single candidate answer and returns:
    {
      "score": 1-5,
      "summary": "...",
      "improvement": "..."
    }
    """
    result = evaluate_with_llm(payload.answer)

    return EvaluationResponse(
        score=result["score"],
        summary=result["summary"],
        improvement=result["improvement"],
    )


@app.post("/rank-candidates", response_model=List[RankedCandidate])
def rank_candidates(payload: RankRequest):
    """
    Takes an array of answers, evaluates each,
    and returns them sorted from highest score to lowest.
    """
    evaluations: List[RankedCandidate] = []

    for ans in payload.answers:
        result = evaluate_with_llm(ans)
        candidate = RankedCandidate(
            answer=ans,
            score=result["score"],
            summary=result["summary"],
            improvement=result["improvement"],
        )
        evaluations.append(candidate)

    # Sort by score (high → low)
    evaluations.sort(key=lambda c: c.score, reverse=True)
    return evaluations
