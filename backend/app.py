"""
==========================================================
DocuMind Backend
==========================================================

Main FastAPI application.

Responsibilities
----------------
• Configure FastAPI
• Configure CORS
• Register API routes
• Start Backend server
"""

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware


from api.routes import router


from utils.logger import logger





app = FastAPI(

    title="DocuMind Backend",

    description="AI Document Intelligence Backend",

    version="3.0.0"

)









# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)









# ---------------------------------------------------------
# Register Routes
# ---------------------------------------------------------

app.include_router(

    router

)









# ---------------------------------------------------------
# Startup
# ---------------------------------------------------------

@app.on_event("startup")

async def startup():


    logger.info(

        "===================================="

    )


    logger.info(

        "DocuMind Backend Started"

    )


    logger.info(

        "API Documentation: /docs"

    )


    logger.info(

        "===================================="

    )









# ---------------------------------------------------------
# Shutdown
# ---------------------------------------------------------

@app.on_event("shutdown")

async def shutdown():


    logger.info(

        "DocuMind Backend Shutdown"

    )









# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")

async def root():


    return {


        "application":

            "DocuMind Backend",


        "version":

            "3.0.0",


        "status":

            "running"


    }









# ---------------------------------------------------------
# Development Server
# ---------------------------------------------------------

if __name__ == "__main__":


    import uvicorn



    uvicorn.run(

        "app:app",

        host="0.0.0.0",

        port=8000,

        reload=True

    )