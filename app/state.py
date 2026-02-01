from pydantic import BaseModel, Field
from typing import Literal, Optional

Node = Literal[
    "WELCOME",
    "INTENT_DETECTION",
    "PSYCHOLOGICAL_SUPPORT",
    "MOOD_CHECK",
    "MOOD_EVALUATION",
    "WELLNESS_ACTION",
    "ESCALATION_CHECK",
    "HUMAN_ESCALATION",
    "END",
]

Intent = Literal[
    "feel_lonely",
    "feel_sad",
    "feel_anxious",
    "daily_checkin",
    "emergency",
    "unknown",
]

class Context(BaseModel):
    needs_monitoring: bool = False
    mood_score: Optional[int] = None
    low_mood_days: int = 0
    last_intent: Intent = "unknown"

class Session(BaseModel):
    session_id: str
    node: Node = "WELCOME"
    context: Context = Field(default_factory=Context)
