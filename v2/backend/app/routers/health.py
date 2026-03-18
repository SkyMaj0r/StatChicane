"""
app/routers/health.py

Health-check router — verifies live connectivity to MySQL and Redis.
No business logic; connection probes only.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.database import test_db_connection
from app.redis_client import test_redis_connection

router = APIRouter(tags=["health"])


# ---------------------------------------------------------------------------
# Database health check
# ---------------------------------------------------------------------------


@router.get("/api/health/db")
async def health_db() -> JSONResponse:
    """Verify that the MySQL connection is live (SELECT 1)."""
    result = test_db_connection()
    status_code = 200 if result["status"] == "ok" else 503
    return JSONResponse(content=result, status_code=status_code)


# ---------------------------------------------------------------------------
# Redis health check
# ---------------------------------------------------------------------------


@router.get("/api/health/redis")
async def health_redis() -> JSONResponse:
    """Verify that the Redis connection is live (PING)."""
    result = test_redis_connection()
    status_code = 200 if result["status"] == "ok" else 503
    return JSONResponse(content=result, status_code=status_code)


# ---------------------------------------------------------------------------
# Combined health check
# ---------------------------------------------------------------------------


@router.get("/api/health/all")
async def health_all() -> JSONResponse:
    """Return combined MySQL + Redis health status."""
    db_result = test_db_connection()
    redis_result = test_redis_connection()

    both_ok = db_result["status"] == "ok" and redis_result["status"] == "ok"

    payload = {
        "database": db_result,
        "redis": redis_result,
        "overall": "ok" if both_ok else "degraded",
    }
    return JSONResponse(content=payload, status_code=200 if both_ok else 503)
