from pathlib import Path
import sys

from fastapi import FastAPI

# Allow `uvicorn app:app` from inside `agent/teamA` by exposing the repo root.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from agent.teamA.routes.agent import router
else:
    from .routes.agent import router

app = FastAPI(
    title="Agent Team A",
    description="Routing agent for the AI Business Intelligence system",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def health_check():
    return {
        "status": "Agent Team A is running",
        "sprint": 1,
        "endpoint": "POST/agent/analyze"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
