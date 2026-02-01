from app.safety import detect_emergency

def detect_intent(text: str) -> str:
    t = (text or "").lower()
    if detect_emergency(t):
        return "emergency"
    if any(k in t for k in ["lonely", "alone", "nobody to talk", "no one to talk"]):
        return "feel_lonely"
    if any(k in t for k in ["sad", "low", "tired of life", "hopeless", "down"]):
        return "feel_sad"
    if any(k in t for k in ["anxious", "worried", "scared", "panic", "nervous"]):
        return "feel_anxious"
    if any(k in t for k in ["how am i today", "daily check", "checkin", "check-in"]):
        return "daily_checkin"
    return "unknown"
