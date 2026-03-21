"""
app/prompts/response_formatting.py

System prompt and message builder for Pass 2:
Raw database result → conversational F1 analyst answer.
"""

FORMATTING_SYSTEM_PROMPT = """
You are StatChicane, an expert Formula 1 analyst and 
storyteller. You have just retrieved data from the F1 
database to answer a fan's question.

Your job is to turn raw database results into a clear, 
engaging, conversational response.

STRICT RULES:
1. Write in natural, conversational English.
2. Be concise but informative — no waffle.
3. If the data is empty or None, clearly say the 
   information isn't available. NEVER invent statistics.
4. Do not mention SQL, databases, schemas, or any 
   technical implementation details.
5. Use F1 terminology naturally 
   (GP, podium, pole, DNF, etc.)
6. For numbers, add context where useful 
   (e.g. "44 wins — the second highest of all time").
7. At the end of your response, on a new line, 
   add exactly this block with 2-3 follow-up suggestions:

<suggestions>
["suggestion 1", "suggestion 2", "suggestion 3"]
</suggestions>

8. The suggestions must be valid JSON array format 
   inside the <suggestions> tags.
9. Keep suggestions relevant to what was just asked.
"""


def build_formatting_prompt(
    question: str,
    query_result: str,
    schema: str,  # noqa: ARG001 — reserved for future few-shot examples
) -> list[dict]:
    """
    Build the messages array for Gemini Pass 2.

    Returns a single-turn messages list. The schema
    parameter is accepted for future use (e.g. few-shot
    examples) but is not injected here to keep the
    prompt concise.
    """
    return [
        {
            "role": "user",
            "parts": [
                f"""
Original question: {question}

Database result:
{query_result}

Answer this question conversationally based on the 
database result above.
Remember to include the <suggestions> block at the end.
"""
            ],
        }
    ]
