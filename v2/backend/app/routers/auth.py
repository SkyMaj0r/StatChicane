"""
app/routers/auth.py

Authentication router — JWT-based registration, login, and token refresh.
Business logic will be added in a later phase; this file is scaffold only.
"""

from fastapi import APIRouter

router = APIRouter(tags=["auth"])


@router.get("/health")
async def auth_health() -> dict:
    """Health check for the auth router."""
    return {"router": "auth", "status": "ok"}
