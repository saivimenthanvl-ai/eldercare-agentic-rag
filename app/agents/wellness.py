def wellness_prompt(rag_snips: list[dict]) -> str:
    context = "\n\n".join([f"- {d['text']}" for d in rag_snips[:4]])
    return f"""Suggest 1–2 simple, realistic actions for an older adult today.
Avoid medical claims. Keep it very short and encouraging.

Reference snippets:
{context}

Return exactly:
1) one small action
2) one optional alternative
"""
