"""
app/redis_client.py

Redis client singleton and cache helper functions.

All helpers wrap operations in try/except so that a Redis outage
degrades gracefully rather than crashing the API.
"""

import json
import logging

import redis

from app.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Client singleton
# ---------------------------------------------------------------------------
# decode_responses=True means all data comes back as Python str, not bytes.

_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def get_cache(key: str):
    """
    Retrieve a cached value by key.

    Returns:
        Parsed JSON object if the key exists, None otherwise.
    """
    try:
        raw = _client.get(key)
        if raw is None:
            return None
        return json.loads(raw)
    except Exception as exc:
        logger.error("Redis GET error for key '%s': %s", key, exc)
        return None


def set_cache(key: str, value: dict, ttl: int) -> None:
    """
    Serialise ``value`` to JSON and store it in Redis with a TTL.

    Args:
        key:   Redis key string.
        value: Dictionary to cache (must be JSON-serialisable).
        ttl:   Time-to-live in seconds.
    """
    try:
        _client.setex(key, ttl, json.dumps(value))
    except Exception as exc:
        logger.error("Redis SET error for key '%s': %s", key, exc)


def delete_cache(key: str) -> None:
    """
    Delete a key from the Redis cache.

    Args:
        key: Redis key string to delete.
    """
    try:
        _client.delete(key)
    except Exception as exc:
        logger.error("Redis DELETE error for key '%s': %s", key, exc)
