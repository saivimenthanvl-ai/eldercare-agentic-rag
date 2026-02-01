from app.safety import enforce_non_clinical

def psych_prompt(user_text: str, rag_snips: list[dict]) -> str:
    context = "\n\n".join([f"- {d['text']}" for d in rag_snips[:3]])
    return f"""You are a supportive, non-clinical companion for an older adult.
Do NOT diagnose or claim you are a therapist. Ask gentle open-ended questions.
Use the knowledge snippets if relevant.

User: {user_text}

Knowledge snippets:
{context}

Write 2-4 short sentences, warm tone, then ask one gentle question.
"""

def postprocess(output: str) -> str:
    return enforce_non_clinical(output)
