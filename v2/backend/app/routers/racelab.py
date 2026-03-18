"""
app/routers/racelab.py

Race Lab router — FastF1 telemetry ingestion and visualisation endpoints.
Business logic will be added in a later phase; this file is scaffold only.
"""

from fastapi import APIRouter

router = APIRouter(tags=["racelab"])


@router.get("/health")
async def racelab_health() -> dict:
    """Health check for the racelab router."""
    return {"router": "racelab", "status": "ok"}
