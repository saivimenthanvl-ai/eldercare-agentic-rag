EMERGENCY_KEYWORDS = [
    "want to die", "can't go on", "cant go on", "kill myself", "suicide", "end my life"
]

def detect_emergency(text: str) -> bool:
    t = (text or "").lower()
    return any(k in t for k in EMERGENCY_KEYWORDS)

def enforce_non_clinical(output: str) -> str:
    # Keep it simple: ensure we do not claim diagnosis/treatment.
    banned = ["diagnose", "prescribe", "i am a doctor", "guarantee", "cure"]
    out = output
    for b in banned:
        out = out.replace(b, "")
    return out
