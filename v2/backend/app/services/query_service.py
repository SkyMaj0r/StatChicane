"""
app/services/query_service.py

Safe SQL execution against MySQL.

Validates every query before execution (allow-list approach:
SELECT only, no forbidden keywords, no User table access),
then returns results as a formatted string suitable for the
LLM in Pass 2, along with a confidence level.
"""

import logging

from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety configuration
# ---------------------------------------------------------------------------

# Table names that must never be queried
FORBIDDEN_TABLES = ["user", "users"]

# DML / DDL keywords that must not appear in queries
_FORBIDDEN_KEYWORDS = frozenset([
    "drop", "delete", "insert", "update",
    "truncate", "alter", "create", "exec",
    "execute", "grant", "revoke",
])

# Maximum rows forwarded to the LLM (keeps context manageable)
_MAX_LLM_ROWS = 50


# ---------------------------------------------------------------------------
# Safety validation
# ---------------------------------------------------------------------------


def is_safe_query(sql: str) -> bool:
    """
    Return True only if the SQL is a safe SELECT query.

    Checks:
    1. Must start with SELECT (or be the no_data sentinel).
    2. Must not contain any forbidden DML/DDL keywords.
    3. Must not reference the User table.
    """
    sql_lower = sql.lower().strip()

    if not sql_lower.startswith("select"):
        return False

    # Word-boundary check: wrap in spaces so "drop" in "teardrop" doesn't match
    padded = f" {sql_lower} "
    for keyword in _FORBIDDEN_KEYWORDS:
        if f" {keyword} " in padded:
            logger.warning("Blocked keyword '%s' found in query", keyword)
            return False

    for table in FORBIDDEN_TABLES:
        if table in sql_lower:
            logger.warning("Blocked forbidden table '%s' in query", table)
            return False

    return True


# ---------------------------------------------------------------------------
# Query execution
# ---------------------------------------------------------------------------


def execute_query(sql: str, db: Session) -> tuple[str, str]:
    """
    Execute a validated SQL query and return results for the LLM.

    Args:
        sql: A SQL SELECT string (already cleaned of markdown fences).
        db:  An active SQLAlchemy Session.

    Returns:
        Tuple of:
            result_str  — Human-readable table of rows (or an error message).
            confidence  — One of "high", "low", "no_data".

    Raises:
        Exception: Re-raises any SQLAlchemy execution error so the router
                   can catch it and trigger the SQL retry loop.
    """
    # ── Sentinel: LLM has indicated the question can't be answered ──────────
    if "no_data_available" in sql.lower():
        return "No data available for this question.", "no_data"

    # ── Safety gate ────────────────────────────────────────────────────────
    if not is_safe_query(sql):
        logger.warning("Blocked unsafe query: %.100s", sql)
        return "Query blocked for safety reasons.", "low"

    # ── Execute ────────────────────────────────────────────────────────────
    try:
        result = db.execute(text(sql))
        rows = result.fetchall()
        columns = list(result.keys())

        if not rows:
            return "Query returned no results.", "low"

        # Build a pipe-separated table string (easy for the LLM to parse)
        header = " | ".join(columns)
        separator = "-" * len(header)

        data_rows = [
            " | ".join(
                str(val) if val is not None else "N/A" for val in row
            )
            for row in rows[:_MAX_LLM_ROWS]
        ]

        result_str = f"{header}\n{separator}\n" + "\n".join(data_rows)

        if len(rows) > _MAX_LLM_ROWS:
            result_str += f"\n... ({len(rows) - _MAX_LLM_ROWS} more rows)"

        confidence = "high" if rows else "no_data"
        logger.info(
            "Query returned %d row(s), confidence: %s", len(rows), confidence
        )
        return result_str, confidence

    except Exception:
        logger.exception("Query execution error for SQL: %.100s", sql)
        raise
