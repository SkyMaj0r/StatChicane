"""
app/routers/ask.py

Ask router — natural-language F1 query pipeline powered by Gemini.
Business logic will be added in a later phase; this file is scaffold only.
"""

from fastapi import APIRouter

router = APIRouter(tags=["ask"])


@router.get("/health")
async def ask_health() -> dict:
    """Health check for the ask router."""
    return {"router": "ask", "status": "ok"}
