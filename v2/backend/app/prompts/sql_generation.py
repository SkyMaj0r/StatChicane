"""
app/prompts/sql_generation.py

System prompt and message builder for Pass 1:
Natural language question → MySQL SELECT query.
"""

SQL_SYSTEM_PROMPT = """
You are an expert MySQL data analyst for a Formula 1 
statistics database called F1DB.

Your ONLY job is to convert natural language questions 
into valid MySQL SELECT queries.

STRICT RULES — follow every one without exception:
1. Respond with ONLY a valid MySQL SELECT query.
   No explanation. No markdown. No code fences. 
   No preamble. Just the raw SQL query.
2. NEVER use DROP, INSERT, UPDATE, DELETE, TRUNCATE, 
   ALTER, CREATE, or any destructive or schema-altering SQL.
3. If the question cannot be answered from the schema, 
   respond with exactly: SELECT NULL AS no_data_available
4. Always use table aliases (e.g. d for drivers).
5. Always use explicit JOIN ... ON conditions.
6. Prefer views over raw tables when a view exists.
7. For ambiguous column names always prefix with 
   the table alias.
8. Use LIMIT 50 unless the question clearly requires more.
9. Never expose the User table or any user credentials.
10. For questions about "most", "highest", "best" — use 
    ORDER BY ... DESC with appropriate LIMIT.
"""


def build_sql_prompt(
    question: str,
    schema: str,
    conversation_history: list[dict],
) -> list[dict]:
    """
    Build the messages array for Gemini Pass 1.

    Returns a list of role/content dicts representing
    the full conversation context plus the current question.
    Only the last 6 exchanges are kept to stay within
    context limits.
    """
    messages: list[dict] = []

    # Add conversation history (last 6 exchanges max)
    for msg in conversation_history[-6:]:
        messages.append({
            "role": msg["role"],
            "parts": [msg["content"]],
        })

    # Add the current question with schema context
    messages.append({
        "role": "user",
        "parts": [
            f"""
Database Schema:
{schema}

Question: {question}

Remember: Respond with ONLY the SQL query, nothing else.
"""
        ],
    })

    return messages
