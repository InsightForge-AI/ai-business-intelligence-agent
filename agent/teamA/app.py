from fastapi import FastAPI
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
