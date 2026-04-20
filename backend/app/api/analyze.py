from fastapi import APIRouter
from pydantic import BaseModel
import concurrent.futures

from app.services.cv_service import run_cv
from app.services.agent_service import run_agent
from app.services.ml_service import run_ml
from app.services.nlp_service import run_nlp
from app.services.rag_service import run_rag

router = APIRouter()


class AnalyzeRequest(BaseModel):
    query: str


# timeout limit (seconds)
TIMEOUT = 5


def safe_execute(func, query, module_name):

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:

            future = executor.submit(func, query)

            result = future.result(timeout=TIMEOUT)

            return result

    except concurrent.futures.TimeoutError:

        return {
            "error": f"{module_name} timeout",
            "fallback": "default response"
        }

    except Exception as e:

        return {
            "error": f"{module_name} failed",
            "details": str(e),
            "fallback": "safe response"
        }



@router.post("/analyze")
def analyze(request: AnalyzeRequest):

    try:

        # ---------- Agent Call ----------
        try:
            agent_results = run_agent(request.query)

        except Exception as e:

            agent_results = {
                "modules": ["nlp"],  # fallback
                "error": "agent failed",
                "details": str(e)
            }


        # ---------- Support both formats ----------
        action = agent_results.get("action")
        modules = agent_results.get("modules")

        # convert old format -> new format
        if not modules and action:
            modules = [action]

        # fallback
        if not modules:
            modules = ["nlp"]


        module_outputs = {}


        # ---------- Module Execution ----------
        for module in modules:

            if module == "nlp":

                module_outputs["nlp"] = safe_execute(
                    run_nlp, request.query, "nlp"
                )


            elif module == "ml":

                module_outputs["ml"] = safe_execute(
                    run_ml, request.query, "ml"
                )


            elif module == "rag":

                module_outputs["rag"] = safe_execute(
                    run_rag, request.query, "rag"
                )


            elif module == "cv":

                module_outputs["cv"] = safe_execute(
                    run_cv, request.query, "cv"
                )


            else:

                module_outputs[module] = {
                    "error": "module not implemented"
                }


        # ---------- Final Response ----------
        return {

            "query": request.query,

            "agent": agent_results,

            "module_results": module_outputs,

            "status": "success"

        }


    except Exception as e:

        # ---------- Global fallback ----------
        return {

            "query": request.query,

            "status": "failed",

            "fallback": {

                "modules": ["nlp", "ml", "rag", "cv"],

                "message": "system fallback response"

            },

            "error": str(e)

        }
