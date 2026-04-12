from fastapi import FastAPI

# Support both `python -m uvicorn agent.teamA.app:app` from the repo root
# and direct local execution from inside `agent/teamA`.
try:
    from .routes.agent import router
except ImportError:
    from routes.agent import router

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
