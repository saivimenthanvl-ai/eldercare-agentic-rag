import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from app.state import Session
from app.rag.store import RagStore
from app.llm_watsonx import WatsonxLLM

from app.agents.orchestrator import detect_intent
from app.agents.monitoring import mood_check_text
from app.agents.psych_support import psych_prompt, postprocess
from app.agents.wellness import wellness_prompt
from app.agents.escalation import escalation_text

load_dotenv()

app = FastAPI(title="ElderCare Agentic RAG API")

SESSIONS: dict[str, Session] = {}

rag = RagStore(os.getenv("RAG_INDEX_DIR", "./data/index"))
llm = WatsonxLLM()

@app.on_event("startup")
def _load():
    rag.load()

class StartReq(BaseModel):
    session_id: str

class StepReq(BaseModel):
    session_id: str
    user_text: str

@app.post("/session/start")
def start(req: StartReq):
    s = Session(session_id=req.session_id)
    SESSIONS[req.session_id] = s
    # WELCOME node response
    s.node = "INTENT_DETECTION"
    return {"messages": ["Hello. I’m here to support you.", "How are you feeling today?"], "node": s.node, "context": s.context.model_dump()}

@app.post("/rag/search")
def rag_search(payload: dict):
    q = payload.get("query", "")
    k = int(payload.get("k", 5))
    return {"results": rag.search(q, k)}

@app.post("/chat/step")
def step(req: StepReq):
    s = SESSIONS.get(req.session_id) or Session(session_id=req.session_id)
    SESSIONS[req.session_id] = s

    # 1) intent detection always runs on new user input
    intent = detect_intent(req.user_text)
    s.context.last_intent = intent

    # Emergency: immediate escalation
    if intent == "emergency":
        resources = rag.search("India mental health helpline Tele MANAS AASRA", 5)
        s.node = "HUMAN_ESCALATION"
        return {"messages": [escalation_text(resources)], "node": s.node, "context": s.context.model_dump()}

    # 2) psychological support
    if intent in ("feel_lonely", "feel_sad", "feel_anxious", "unknown"):
        snips = rag.search("safe supportive language older adult non-clinical", 5)
        prompt = psych_prompt(req.user_text, snips)
        out = llm.generate(prompt)
        out = postprocess(out)
        s.context.needs_monitoring = True
        s.node = "MOOD_CHECK"
        return {"messages": [out, mood_check_text()], "node": s.node, "context": s.context.model_dump()}

    # 3) daily check-in → mood check
    if intent == "daily_checkin":
        s.context.needs_monitoring = True
        s.node = "MOOD_CHECK"
        return {"messages": ["Thank you for checking in with me.", mood_check_text()], "node": s.node, "context": s.context.model_dump()}

    # default
    return {"messages": ["Thank you for sharing that with me."], "node": s.node, "context": s.context.model_dump()}
