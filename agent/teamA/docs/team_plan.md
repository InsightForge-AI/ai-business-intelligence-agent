# Agent Team A — Sprint 1 Team Plan

**Project:** AI Business Intelligence Agent
**Sprint:** 1
**Team Lead:** Prabhu Teja
**Team Size:** 4 members (Lead + 3)
**Goal:** Build a routing agent that reads a user query and decides which service handles it (nlp / ml / cv). No actual API calls in Sprint 1.

---

## Current Folder Structure

```
agent/teamA/
├── .gitignore
├── requirements.txt
├── app.py                  ← Team Lead owns this
├── config.py               ← Team Lead owns this
├── __init__.py
├── routes/
│   └── agent.py            ← Member B owns this
├── schemas/
│   └── models.py           ← Member C owns this
├── services/
│   └── decision.py         ← Member A owns this
├── docs/
│   └── api_reference.md    ← Member D owns this
└── tests/
    └── test_agent.py       ← Member D owns this
```

---

## Task Assignments — WHO OWNS WHAT

| Member | Role | Branch | File(s) | Task |
|--------|------|--------|---------|------|
| Prabhu Teja | Team Lead | `teamA/agent-setup` | `app.py`, `config.py`, `requirements.txt`, `.gitignore` | Set up the base FastAPI app, constants, and project config. Review all PRs. |
| Member A | Routing Logic | `teamA/agent-decision` | `services/decision.py` | Write the `decide(query)` function using keyword matching from `config.py` |
| Member B | API Layer | `teamA/agent-routes` | `routes/agent.py` | Write the `POST /agent/analyze` endpoint. Import `decide()` and return `{"action": "..."}` |
| Member C | Data Models | `teamA/agent-schemas` | `schemas/models.py` | Write `AnalyzeRequest` and `AnalyzeResponse` Pydantic models |
| Member D | Tests & Docs | `teamA/agent-testing` | `tests/test_agent.py`, `docs/api_reference.md` | Write 18 pytest tests. Keep API reference doc in sync with code. |

**Golden Rule: One file = one owner.**
Never edit another member's file without their knowledge. If you must, discuss first. Commit message must say why. Team lead approves.

---

## What Each Member Must Write

### Team Lead — `config.py`
```python
ROUTING_KEYWORDS = {
    "nlp": ["review", "feedback", "sentiment", "opinion", "comment", "text"],
    "ml":  ["sales", "revenue", "trend", "data", "performance", "product", "profit", "analytics"],
    "cv":  ["image", "photo", "picture", "visual", "cv", "object"]
}

ROUTE_MESSAGES = {
    "nlp":     "Route to NLP service for text analysis",
    "ml":      "Route to ML service for data analysis",
    "cv":      "Route to CV service for image analysis",
    "unknown": "No matching module found"
}
```

### Team Lead — `app.py`
```python
from fastapi import FastAPI
from routes.agent import router

app = FastAPI(title="Agent Team A", version="1.0.0")
app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "Agent Team A is running", "sprint": 1}
```

### Member A — `services/decision.py`
```python
from config import ROUTING_KEYWORDS

def decide(query: str) -> str:
    q = query.lower()
    for module, keywords in ROUTING_KEYWORDS.items():
        if any(keyword in q for keyword in keywords):
            return module
    return "unknown"
```

### Member B — `routes/agent.py`
```python
from fastapi import APIRouter, HTTPException
from schemas.models import AnalyzeRequest, AnalyzeResponse
from services.decision import decide

router = APIRouter()

@router.post("/agent/analyze", response_model=AnalyzeResponse)
def agent_analyze(request: AnalyzeRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Field 'query' must not be empty")
    return AnalyzeResponse(action=decide(request.query))
```

### Member C — `schemas/models.py`
```python
from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    query: str = Field(description="User query to route to the correct service")

class AnalyzeResponse(BaseModel):
    action: str = Field(description="Resolved module: nlp, ml, cv, or unknown")
```

### Member D — `tests/test_agent.py`
Write pytest tests covering:
- NLP routing: review, sentiment, text, feedback
- ML routing: sales, revenue, data, analytics
- CV routing: image, photo, visual
- Unknown routing: random query, weather
- Error handling: empty query → 400
- Contract: response has only `action` key

---

## Dependency Order — Who Must Finish First

```
Team Lead (config.py + app.py)
    ↓
Member C (schemas/models.py) — needed by Member B
Member A (services/decision.py) — needed by Member B
    ↓
Member B (routes/agent.py) — depends on A and C
    ↓
Member D (tests/test_agent.py) — depends on all above
```

Do NOT start your task until the task above yours is merged into `dev`.

---

## Git Workflow — Step by Step for Every Member

### One-time setup (do this once)

```bash
git clone https://github.com/InsightForge-AI/ai-business-intelligence-agent
cd ai-business-intelligence-agent
```

---

### Every feature starts here

**Step 1 — Switch to dev and pull latest**
```bash
git checkout dev
git pull origin dev
```
Always start from fresh dev. Never branch from stale code.

**Step 2 — Create your feature branch**

| Member | Command |
|--------|---------|
| Team Lead | `git checkout -b teamA/agent-setup` |
| Member A | `git checkout -b teamA/agent-decision` |
| Member B | `git checkout -b teamA/agent-routes` |
| Member C | `git checkout -b teamA/agent-schemas` |
| Member D | `git checkout -b teamA/agent-testing` |

Branch name must start with `teamA/` exactly.

**Step 3 — Navigate to your folder**
```bash
cd agent/teamA/
```
Work ONLY inside `agent/teamA/`. Do NOT touch other teams' folders.

**Step 4 — Write your code**

Write only your assigned file(s). See the task table above for what to write.
Follow the code style rules:
- Type hints on all functions
- No print statements
- No hardcoded strings — import from `config.py`
- Snake_case everywhere

**Step 5 — Stage and commit**
```bash
git add .
git commit -m "feat: add decision logic with keyword routing"
```

Commit message format: `type: short description`

| Type | When to use |
|------|-------------|
| `feat` | Adding new code |
| `fix` | Fixing a bug |
| `docs` | Updating documentation |
| `test` | Adding or fixing tests |
| `refactor` | Restructuring code without changing behavior |

Commit often. Small commits are easier to review.

**Step 6 — Push your branch**
```bash
git push -u origin teamA/agent-decision
```
After the first push, use just `git push`.
Without pushing, your work does not exist for the team.

**Step 7 — Create a Pull Request on GitHub**

1. Go to the GitHub repository
2. Click **Compare & pull request**
3. Set **Base branch → `dev`**
4. Set **Compare → your branch**
5. Write a clear PR title: `feat: add decision logic`
6. In the description, write:
   - What you built
   - What to test
   - Any notes or blockers
7. Click **Create pull request**
8. Send the PR link to the team lead on WhatsApp/Teams

**Step 8 — Fix review comments**

If the team lead requests changes:
```bash
# Edit your file
git add .
git commit -m "fix: address review comments"
git push
```
The PR updates automatically. Reply in the PR comments when a fix is done.

**Step 9 — After PR is merged, sync up**
```bash
git checkout dev
git pull origin dev
```
Always pull after a merge to stay in sync.

---

## Pull Request Checklist — Before you raise a PR

- [ ] Code runs without error (`python app.py` or `uvicorn app:app`)
- [ ] No syntax errors
- [ ] Your file follows the code style (type hints, no print, snake_case)
- [ ] You only changed files assigned to you
- [ ] Commit message follows the format
- [ ] Base branch is set to `dev` (not `main`)
- [ ] PR description explains what you built

---

## Team Lead Review Checklist

- [ ] Code follows the API contract (output is `{"action": "..."}` only)
- [ ] No hardcoded strings outside `config.py`
- [ ] No imports from FastAPI inside `services/decision.py`
- [ ] No routing logic inside `routes/agent.py`
- [ ] Tests cover all routes + error cases
- [ ] PR targets `dev`, not `main`

---

## Important Rules

- Never push directly to `main`
- Never push directly to `dev`
- Always pull before starting any new work
- One feature = one branch
- One file = one owner
- Work only inside `agent/teamA/`
- All strings come from `config.py` — no hardcoding anywhere else

---

## Summary Flow

```
clone → checkout dev → pull → create branch → write code → commit → push → raise PR → review → fix → merge → pull dev → repeat
```
