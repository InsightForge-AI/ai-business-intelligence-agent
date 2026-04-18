from fastapi import APIRouter
from pydantic import BaseModel

from app.services.cv_service import run_cv
from app.services.agent_service import run_agent
from app.services.ml_service import run_ml
from app.services.nlp_service import run_nlp
from app.services.rag_service import run_rag

router = APIRouter()


class AnalyzeRequest(BaseModel):
    query: str


@router.post("/analyze")

def analyze(request: AnalyzeRequest):

    try:

        agent_results = run_agent(request.query)

        action = agent_results.get("action")

        result = None


        if action == "nlp":

            result = run_nlp(request.query)


        elif action == "ml":

            result = run_ml(request.query)


        elif action == "rag":

            result = run_rag(request.query)


        elif action == "cv":

            result = run_cv(request.query)


        else:

            result = {

                "message": "No module matched",

                "agent_output": agent_results

            }


        return {

            "agent": agent_results,

            "module_results": result

        }


    except Exception as e:

        return {

            "error": str(e)

        }