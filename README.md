# ElderCare Agentic RAG

Safety-first, retrieval-grounded emotional support for older adults.

## Overview

**ElderCare Agentic RAG** is a lightweight multi-agent conversational support system designed for older adults who may feel lonely, anxious, emotionally low, or in need of a gentle daily check-in. The system combines:

- **deterministic safety routing** for crisis-first handling,
- **retrieval-augmented generation (RAG)** for grounded support and wellness suggestions,
- **session-aware agent orchestration** for emotional support, mood monitoring, and escalation.

The goal is not to replace clinicians or caregivers. The goal is to provide a **safe, non-clinical first layer of support** that can respond empathetically, offer small actionable wellness steps, and escalate appropriately when emotional risk is detected.

---

## Problem Statement

Many older adults experience:

- loneliness and social isolation,
- anxiety or low mood,
- difficulty reaching the right support quickly,
- generic chatbot responses that are unsafe, ungrounded, or overly clinical.

Most conversational systems are not designed around **elder-specific emotional support**, **non-clinical safety constraints**, and **human escalation pathways**.

This project addresses that gap with a focused architecture that prioritizes:

1. **Safety before fluency**
2. **Grounded responses before generic generation**
3. **Escalation before over-automation**

---

## What the App Does

The application starts a support session, detects the user’s emotional intent, and routes the conversation to the right behavior:

- **Emergency detection** → immediately surfaces human-help guidance and crisis resources.
- **Lonely / sad / anxious states** → generates a warm, non-clinical response grounded by retrieved knowledge.
- **Daily check-in** → asks the user to rate their mood.
- **Monitoring flow** → prepares the conversation for follow-up mood evaluation and potential escalation.

The API currently exposes endpoints to:

- start a session,
- step through the chat,
- search the RAG knowledge base directly.

---

## Key Features

### 1) Safety-first intent routing
The orchestrator checks for emergency language before anything else. Crisis signals bypass the normal conversational loop and trigger escalation immediately.

### 2) Non-clinical emotional support
The assistant is explicitly constrained to avoid diagnosis, prescription, and therapist impersonation. It responds with short, supportive, open-ended language.

### 3) Retrieval-Augmented Generation (RAG)
The system retrieves relevant snippets from a local knowledge base before generating a response. This improves grounding and reduces empty, generic replies.

### 4) Mood check workflow
After emotionally sensitive interactions, the system asks the user to rate their mood on a 1–10 scale so the next stage can monitor persistence of low mood.

### 5) Local knowledge base for India-specific resources
The current knowledge base includes Indian support references such as Tele MANAS and AASRA, plus basic wellness guidelines.

### 6) IBM watsonx.ai integration scaffold
The repo is prepared to connect to watsonx.ai models, making it easy to swap the placeholder generation path for an enterprise-grade hosted LLM.

---

## Architecture

```text
User Input
   |
   v
FastAPI API Layer
   |
   v
Intent Detection / Safety Router
   |-------------------------------> Emergency Escalation Agent
   |
   |----> Psychological Support Agent
   |            |
   |            v
   |        RAG Search (FAISS + MiniLM)
   |            |
   |            v
   |        watsonx / fallback response
   |
   |----> Monitoring Prompt
   |
   |----> Wellness Action Agent
   |
   v
Session State Update
```

### Core modules

- `app/main.py` — FastAPI app and API endpoints
- `app/state.py` — session and conversation state schema
- `app/safety.py` — emergency keyword detection and non-clinical filtering
- `app/agents/orchestrator.py` — intent routing logic
- `app/agents/psych_support.py` — prompt builder for supportive responses
- `app/agents/monitoring.py` — mood check prompt
- `app/agents/escalation.py` — escalation response formatter
- `app/agents/wellness.py` — small wellness action prompt
- `app/rag/ingest.py` — knowledge ingestion and FAISS indexing
- `app/rag/store.py` — retrieval interface
- `app/llm_watsonx.py` — watsonx.ai model wrapper scaffold

---

## Current Routing Logic

The intended orchestration policy is:

1. **Emergency always wins**
2. **Emotional distress routes to supportive conversation first**
3. **Support is followed by mood monitoring**
4. **Persistently low mood increases escalation risk**
5. **Repeated low mood triggers human escalation**
6. **Otherwise the system suggests a small wellness action**

This routing policy is also documented in the repo’s orchestration notes.

---

## Repository Structure

```text
eldercare-agentic-rag/
├── app/
│   ├── agents/
│   │   ├── escalation.py
│   │   ├── monitoring.py
│   │   ├── orchestrator.py
│   │   ├── psych_support.py
│   │   └── wellness.py
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── prompts.py
│   │   └── store.py
│   ├── llm_watsonx.py
│   ├── main.py
│   ├── safety.py
│   └── state.py
├── data/
│   ├── index/
│   └── knowledge/
│       ├── resources_india.md
│       ├── safety_policy.md
│       └── wellness_guidelines.md
├── .env.example
├── openapi.tool.yaml
├── requirements.txt
├── Orchestrator Routing Logic – ElderCare AI.md
├── Watsonx Hackathon.png
├── Psychological Support.png
└── Human Esclation Prompt.png
```

---

## Tech Stack

### Backend
- **FastAPI**
- **Uvicorn**
- **Pydantic**
- **python-dotenv**
- **requests**

### Retrieval
- **sentence-transformers**
- **all-MiniLM-L6-v2** embeddings
- **FAISS (CPU)** vector index
- **NumPy**

### LLM / AI
- **IBM watsonx.ai integration scaffold**
- default configured model: **granite-3-8b-instruct**

### Orchestration Pattern
- rule-based safety router
- lightweight multi-agent flow
- session-state tracking
- retrieval-grounded response generation

---

## Setup

### 1) Clone the repo

```bash
git clone https://github.com/saivimenthanvl-ai/eldercare-agentic-rag.git
cd eldercare-agentic-rag
```

### 2) Create environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

### 3) Configure environment variables

Create a `.env` file based on `.env.example`:

```env
WATSONX_APIKEY=REPLACE_ME
WATSONX_PROJECT_ID=REPLACE_ME
WATSONX_REGION=dallas
WATSONX_MODEL_ID=granite-3-8b-instruct

RAG_INDEX_DIR=./data/index
RAG_KNOWLEDGE_DIR=./data/knowledge
```

---

## Build the RAG Index

If you update files inside `data/knowledge`, rebuild the FAISS index:

```bash
python -m app.rag.ingest
```

This will:

- read `.md` and `.txt` files from the knowledge folder,
- chunk the text,
- embed each chunk using `all-MiniLM-L6-v2`,
- store vectors in `data/index/faiss.index`,
- store chunk metadata in `data/index/docs.jsonl`.

---

## Run the App

```bash
uvicorn app.main:app --reload
```

Default server:

```text
http://localhost:8000
```

---

## API Endpoints

### `POST /session/start`
Start a new conversation session.

**Request**

```json
{
  "session_id": "user-001"
}
```

**Response**

```json
{
  "messages": [
    "Hello. I’m here to support you.",
    "How are you feeling today?"
  ],
  "node": "INTENT_DETECTION",
  "context": {
    "needs_monitoring": false,
    "mood_score": null,
    "low_mood_days": 0,
    "last_intent": "unknown"
  }
}
```

---

### `POST /chat/step`
Send the next user message and let the orchestrator decide what happens next.

**Request**

```json
{
  "session_id": "user-001",
  "user_text": "I feel lonely and have no one to talk to"
}
```

**Typical behavior**

- detect emotional intent,
- retrieve grounding snippets,
- generate a non-clinical response,
- ask for a mood score.

---

### `POST /rag/search`
Search the RAG knowledge base directly.

**Request**

```json
{
  "query": "India mental health helpline",
  "k": 5
}
```

**Response**

```json
{
  "results": [
    {
      "id": "resources_india.md:0",
      "source": "resources_india.md",
      "text": "Tele MANAS Mental Health Helpline: 14416 ..."
    }
  ]
}
```

---

## Safety Design

This project is built around a deliberate safety posture:

- emergency phrases are checked before normal generation,
- the assistant avoids diagnosis and treatment claims,
- the support style is intentionally non-clinical,
- crisis-like situations are redirected toward human support,
- wellness suggestions are small, realistic, and low-risk.

This is an important design choice: a support system for vulnerable users should not optimize for cleverness at the expense of predictability.

---

## Example Knowledge Base Content

The current repo includes examples such as:

- **Tele MANAS** mental health helpline
- **AASRA** helpline
- wellness suggestions like:
  - brief sunlight exposure,
  - a short walk if safe,
  - breathing exercise,
  - contacting a trusted person.

---

## Demo Narrative

A typical demo flow looks like this:

1. User starts a session.
2. User says they feel lonely or anxious.
3. Router classifies the intent.
4. RAG retrieves grounded support snippets.
5. The support agent responds empathetically.
6. The monitoring agent asks for a 1–10 mood score.
7. If risk remains high across repeated low scores, the system escalates.

This makes the project easy to present in hackathons because the safety story, architecture story, and user story are all clear.

---

## What Is Technically Interesting

This project is interesting because it does **not** treat agentic AI as “just connect an LLM to tools.”

Instead, it separates responsibilities:

- **safety routing is deterministic**,
- **support generation is constrained**,
- **retrieval adds grounding**,
- **state enables monitoring over time**,
- **escalation remains explicit and auditable**.

That design choice matters. In sensitive domains, predictable orchestration is often more valuable than raw model creativity.

---

## Current Limitations

This repository is a strong MVP/prototype, but not yet a finished production system.

Current gaps include:

- watsonx generation is still scaffolded and needs full API wiring,
- mood-score parsing and repeated low-mood escalation are only partially connected,
- no persistent database is used yet,
- no authentication or caregiver dashboard yet,
- no full evaluation metrics or red-team safety benchmark yet,
- `safety_policy.md` and `README.md` are currently minimal in the repo.

These are normal prototype-stage gaps, but they should be stated honestly.

---

## Roadmap

Planned next improvements:

- full watsonx.ai endpoint integration,
- robust mood-score extraction and tracking across sessions,
- caregiver notification or dashboard,
- multilingual elder support,
- stronger safety policy coverage,
- evaluation suite for crisis detection and response quality,
- deployment with secure secrets and observability.

---

## Suggested Use Cases

- elder emotional check-in assistant,
- first-line support companion,
- caregiver-support triage system,
- retrieval-grounded wellbeing assistant,
- hackathon demo for safe agent orchestration.

---

## Important Disclaimer

This assistant is **not** a doctor, therapist, or emergency service.
It is a **non-clinical emotional support and escalation system**.
If a user is in immediate danger, the system should direct them to local emergency services or trusted human support immediately.

---

## Screenshots / Assets

You can embed the existing visuals already present in the repository:

```md
![Hackathon Architecture](./Watsonx%20Hackathon.png)
![Psychological Support Flow](./Psychological%20Support.png)
![Human Escalation Flow](./Human%20Esclation%20Prompt.png)
```

---

## Why This Project Matters

Elder support is not only a model problem. It is a systems problem.
A useful assistant in this space must balance empathy, grounding, monitoring, and escalation.

This project shows a practical path toward that balance:

- small enough to understand,
- structured enough to audit,
- safe enough to improve,
- modular enough to extend.

---

## License

Add a license before wider sharing or deployment.

A good default for open collaboration:

```text
MIT License
```

---

## Author

**Sai Vimenthan V L**

If you are using this for a hackathon submission, add:

- project video/demo link,
- presentation link,
- deployment link,
- team member names,
- evaluation results.
