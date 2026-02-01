def escalation_text(resources: list[dict]) -> str:
    lines = ["I’m really glad you reached out.", "You don’t have to handle this alone.", ""]
    lines += ["It may help to speak with a trained professional or someone you trust.",
              "Here are support options available right now:", ""]
    # Include top resource snippets
    for r in resources[:3]:
        lines.append(f"• {r['text'].strip()}")
    lines += ["", "If you’re in immediate danger, please contact local emergency services."]
    return "\n".join(lines)
