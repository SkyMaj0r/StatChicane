"""
app/routers/ask.py

Ask F1 router — full two-pass LLM pipeline.

POST /api/ask/query
  1. Pass 1: Generate SQL from the natural language question (Gemini, temp 0.0)
  2. Execute SQL against MySQL via query_service
  3. On failure: retry up to MAX_SQL_RETRIES times, feeding the error back to
     the LLM so it can self-correct
  4. Pass 2: Format raw rows into a conversational answer (Gemini, temp 0.3)
  5. Return AskResponse with answer, sql_used, suggestions, confidence
"""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ask import AskRequest, AskResponse
from app.services.llm_service import generate_response, generate_sql
from app.services.query_service import execute_query
from app.services.schema_service import get_schema

logger = logging.getLogger(__name__)

router = APIRouter(tags=["ask"])

# Maximum number of SQL regeneration attempts after the first try
MAX_SQL_RETRIES = 2


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


@router.get("/health")
async def health() -> dict:
    """Quick liveness check for the ask router."""
    return {"router": "ask", "status": "ok"}


# ---------------------------------------------------------------------------
# Main endpoint
# ---------------------------------------------------------------------------


@router.post("/query", response_model=AskResponse)
async def ask_query(
    request: AskRequest,
    db: Session = Depends(get_db),
) -> AskResponse:
    """
    Main Ask F1 endpoint — full two-pass pipeline.

    Flow:
      1. Pass 1: Generate SQL from natural language
      2. Execute SQL against MySQL
      3. If SQL fails, retry with error context (max 2 retries)
      4. Pass 2: Format raw results into conversational answer
      5. Return answer, SQL used, suggestions, confidence
    """
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    history = [
        {"role": msg.role, "content": msg.content}
        for msg in request.conversation_history
    ]
    schema = get_schema()

    sql: str | None = None
    query_result: str = ""
    confidence: str = "low"
    last_error: str | None = None

    # ── Pass 1: SQL generation with self-correcting retry loop ─────────────
    for attempt in range(MAX_SQL_RETRIES + 1):
        try:
            if attempt == 0:
                # First attempt: clean generation
                sql = await generate_sql(question, history, schema)
            else:
                # Subsequent attempts: give the LLM its previous SQL and the
                # error message so it can generate a corrected query
                logger.info(
                    "SQL retry attempt %d — previous error: %s",
                    attempt,
                    last_error,
                )
                error_context = (
                    f"{question}\n\n"
                    f"Your previous SQL attempt was:\n{sql}\n\n"
                    f"It failed with this error: {last_error}\n\n"
                    f"Please fix the SQL and try again. "
                    f"Return ONLY the corrected SQL query."
                )
                sql = await generate_sql(error_context, history, schema)

            # ── Execute ────────────────────────────────────────────────────
            query_result, confidence = execute_query(sql, db)
            last_error = None
            break  # Success — exit retry loop

        except Exception as exc:
            last_error = str(exc)
            logger.warning("SQL attempt %d/%d failed: %s", attempt + 1, MAX_SQL_RETRIES + 1, exc)

            if attempt == MAX_SQL_RETRIES:
                logger.error(
                    "All %d SQL attempts exhausted for question: %s",
                    MAX_SQL_RETRIES + 1,
                    question,
                )
                query_result = (
                    "Unable to retrieve data after multiple attempts."
                )
                confidence = "low"

    # ── Pass 2: Format result into conversational answer ───────────────────
    try:
        answer, suggestions = await generate_response(
            question, query_result, schema
        )
    except Exception as exc:
        logger.error("Response formatting (Pass 2) failed: %s", exc)
        answer = (
            "I found some data but had trouble formatting the response. "
            "Please try again."
        )
        suggestions = []

    return AskResponse(
        answer=answer,
        sql_used=sql or "",
        suggestions=suggestions,
        confidence=confidence,
        error=last_error if last_error else None,
    )
