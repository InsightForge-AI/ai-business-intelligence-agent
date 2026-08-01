"""

Entry point for the ML microservice.

Responsibilities
----------------
• Initialize FastAPI
• Register API routes
• Configure application metadata
• Start the ML service
"""

from fastapi import FastAPI

from api.routes import router


app = FastAPI(

    title="DocuMind ML Service",

    description="Machine Learning Service for Business Analytics",

    version="1.0.0"

)


# ---------------------------------------------------------
# Register API Routes
# ---------------------------------------------------------

app.include_router(router)


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------

@app.get("/")
async def root():

    return {

        "service": "DocuMind ML Service",

        "status": "running",

        "version": "1.0.0"

    }