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

from pathlib import Path

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles


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

# allow_credentials is intentionally False: combining a wildcard origin
# with allow_credentials=True makes Starlette reflect back *any* request
# Origin verbatim with credentials allowed, i.e. no real CORS protection.
# The bundled frontend (mounted below at /ui) is same-origin and doesn't
# need this at all -- "*" stays here only for hitting the API directly
# from tools like a separately-hosted frontend, Postman, or curl.
app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

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
# Frontend (static files)
# ---------------------------------------------------------

# Mounted under /ui, not "/", so the existing root/docs/api routes above
# keep working exactly as before -- this only adds a UI, it doesn't
# replace anything.

FRONTEND_DIRECTORY = (

    Path(__file__).resolve().parent.parent / "frontend" / "webpage"

)

if FRONTEND_DIRECTORY.is_dir():

    app.mount(

        "/ui",

        StaticFiles(directory=str(FRONTEND_DIRECTORY), html=True),

        name="ui"

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

            "running",


        "ui":

            "/ui"


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