from fastapi import FastAPI
from routes.agent_routes import router

app = FastAPI(
    title="Agentic AI Service",
    description="Routing agent for AI Business Intelligence system",
    version="1.0.0"
)

#  Include routes with proper tagging
app.include_router(router, tags=["Agent"])

#  Health check (improved version)
@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "Agentic AI",
        "sprint": 4,
        "endpoint": "POST /agent/analyze"
    }


# Optional: allow running via python file 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )