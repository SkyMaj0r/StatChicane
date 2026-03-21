"""
app/models/ask.py

Pydantic schemas for the Ask F1 endpoint.
"""

from typing import Optional

from pydantic import BaseModel


class ConversationMessage(BaseModel):
    """A single turn in the conversation history."""

    role: str      # "user" or "assistant"
    content: str


class AskRequest(BaseModel):
    """Request body for POST /api/ask/query."""

    question: str
    conversation_history: list[ConversationMessage] = []


class AskResponse(BaseModel):
    """Response body from POST /api/ask/query."""

    answer: str
    sql_used: str
    suggestions: list[str] = []
    confidence: str          # "high" | "medium" | "low" | "no_data"
    error: Optional[str] = None
