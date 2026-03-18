"""
StatChicane v2 — FastAPI entry point.

Registers routers, configures CORS middleware, and exposes a root health check.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, ask, racelab, health

# ---------------------------------------------------------------------------
# App instance
# ---------------------------------------------------------------------------

app = FastAPI(
    title="StatChicane v2 API",
    description="Formula 1 intelligence platform — backend API",
    version="2.0.0",
)

# ---------------------------------------------------------------------------
# CORS middleware
# ---------------------------------------------------------------------------
# CORS_ORIGINS is a comma-separated string in the env; split into a list.

origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Router registration
# ---------------------------------------------------------------------------

app.include_router(auth.router, prefix="/api/auth")
app.include_router(ask.router,  prefix="/api/ask")
app.include_router(racelab.router, prefix="/api/racelab")
app.include_router(health.router)

# ---------------------------------------------------------------------------
# Root health check
# ---------------------------------------------------------------------------

@app.get("/", tags=["health"])
async def root() -> dict:
    """Basic health check — confirms the API is reachable."""
    return {"status": "ok", "app": "StatChicane v2"}
