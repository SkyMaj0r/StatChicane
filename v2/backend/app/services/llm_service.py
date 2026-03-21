"""
app/services/llm_service.py

Core service for all Gemini API communication.

Two-pass architecture:
  Pass 1 — generate_sql():   NL question  → MySQL SELECT
  Pass 2 — generate_response(): raw DB rows → conversational answer

Public entry point for the ask router:
  run_ask_pipeline() — runs Pass 1 and returns the SQL.
  The router executes the SQL, then calls generate_response().
"""

import json
import logging
import re

import google.generativeai as genai

from app.config import settings
from app.prompts.response_formatting import (
    FORMATTING_SYSTEM_PROMPT,
    build_formatting_prompt,
)
from app.prompts.sql_generation import SQL_SYSTEM_PROMPT, build_sql_prompt
from app.services.schema_service import get_schema

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Gemini SDK configuration
# ---------------------------------------------------------------------------

genai.configure(api_key=settings.GEMINI_API_KEY)

# One model instance per pass — different temperatures and token budgets.
sql_model = genai.GenerativeModel(
    model_name=settings.GEMINI_MODEL,
    system_instruction=SQL_SYSTEM_PROMPT,
    generation_config={
        "temperature": 0.0,        # Fully deterministic for SQL
        "max_output_tokens": 1024,
        "top_p": 0.95,
    },
)

formatting_model = genai.GenerativeModel(
    model_name=settings.GEMINI_MODEL,
    system_instruction=FORMATTING_SYSTEM_PROMPT,
    generation_config={
        "temperature": 0.3,        # Slight creativity for narrative answers
        "max_output_tokens": 2048,
        "top_p": 0.95,
    },
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def clean_sql(raw: str) -> str:
    """
    Strip markdown fences the model may add despite instructions.
    Handles ```sql ... ``` and plain ``` ... ``` blocks.
    """
    cleaned = re.sub(
        r"```(?:sql)?\s*([\s\S]*?)\s*```",
        r"\1",
        raw.strip(),
    )
    return cleaned.strip()


def parse_suggestions(raw_answer: str) -> tuple[str, list[str]]:
    """
    Extract the <suggestions> block from a formatted answer.

    Returns:
        (clean_answer, suggestions_list)

    The suggestions block is removed from the answer text so
    the frontend receives clean prose + a structured list separately.
    """
    suggestions: list[str] = []
    clean_answer = raw_answer

    match = re.search(
        r"<suggestions>\s*([\s\S]*?)\s*</suggestions>",
        raw_answer,
    )
    if match:
        try:
            suggestions = json.loads(match.group(1))
        except json.JSONDecodeError:
            logger.warning("Could not parse suggestions JSON — returning empty list")
            suggestions = []
        # Strip the block from the answer
        clean_answer = raw_answer[: match.start()].strip()

    return clean_answer, suggestions


# ---------------------------------------------------------------------------
# Pass 1 — SQL generation
# ---------------------------------------------------------------------------


async def generate_sql(
    question: str,
    conversation_history: list[dict],
    schema: str,
) -> str:
    """
    Convert a natural language question into a MySQL SELECT query.

    Args:
        question: The user's natural language question.
        conversation_history: Previous turn dicts with 'role'/'content' keys.
        schema: F1DB schema string to include as context.

    Returns:
        A raw SQL SELECT string (already stripped of any markdown fences).

    Raises:
        Exception: Propagates any Gemini API error to the caller.
    """
    messages = build_sql_prompt(question, schema, conversation_history)

    try:
        # Pass all prior turns as chat history; send the final user turn
        chat = sql_model.start_chat(history=messages[:-1])
        response = await chat.send_message_async(messages[-1]["parts"][0])
        sql = clean_sql(response.text)
        logger.info("Pass 1 SQL: %.100s", sql)
        return sql
    except Exception:
        logger.exception("Pass 1 (SQL generation) failed")
        raise


# ---------------------------------------------------------------------------
# Pass 2 — Response formatting
# ---------------------------------------------------------------------------


async def generate_response(
    question: str,
    query_result: str,
    schema: str,
) -> tuple[str, list[str]]:
    """
    Turn raw database rows into a conversational F1 answer.

    Args:
        question: The original natural language question.
        query_result: Stringified query result (JSON rows or error message).
        schema: F1DB schema string (reserved for future few-shot examples).

    Returns:
        Tuple of (answer_text, suggestions_list).

    Raises:
        Exception: Propagates any Gemini API error to the caller.
    """
    messages = build_formatting_prompt(question, query_result, schema)

    try:
        chat = formatting_model.start_chat()
        response = await chat.send_message_async(messages[0]["parts"][0])
        answer, suggestions = parse_suggestions(response.text)
        return answer, suggestions
    except Exception:
        logger.exception("Pass 2 (response formatting) failed")
        raise


# ---------------------------------------------------------------------------
# Public pipeline entry point
# ---------------------------------------------------------------------------


async def run_ask_pipeline(
    question: str,
    conversation_history: list[dict],
) -> dict:
    """
    Run Pass 1 of the Ask F1 pipeline.

    Pass 1 converts the question to SQL. The router is responsible
    for executing the SQL against the database, then calling
    generate_response() with the result rows.

    Args:
        question: The user's natural language question.
        conversation_history: Previous turn dicts with 'role'/'content' keys.

    Returns:
        dict with keys:
            sql    — the generated MySQL SELECT string
            schema — the schema string used (passed to generate_response)
    """
    schema = get_schema()
    sql = await generate_sql(question, conversation_history, schema)
    return {
        "sql": sql,
        "schema": schema,
    }
