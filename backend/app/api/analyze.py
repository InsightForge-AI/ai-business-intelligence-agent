from fastapi import APIRouter
from pydantic import BaseModel
import concurrent.futures
import logging
import time

from app.services.cv_service import run_cv
from app.services.agent_service import run_agent
from app.services.ml_service import run_ml
from app.services.nlp_service import run_nlp
from app.services.rag_service import run_rag

router = APIRouter()

logger = logging.getLogger(__name__)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)


class AnalyzeRequest(BaseModel):
    query: str


SERVICE_MAP = {
    "nlp": run_nlp,
    "ml": run_ml,
    "rag": run_rag,
    "cv": run_cv
}


TIMEOUTS = {
    "nlp": 15,
    "ml": 25,
    "rag": 40,
    "cv": 60
}


def execute_with_timeout(service, query, module):

    start_time = time.time()

    try:

        future = executor.submit(service, query)

        result = future.result(
            timeout=TIMEOUTS.get(module, 20)
        )

        execution_time = round(
            time.time() - start_time,
            3
        )

        logger.info(
            f"{module} executed in {execution_time}s"
        )

        return result

    except concurrent.futures.TimeoutError:

        execution_time = round(
            time.time() - start_time,
            3
        )

        logger.error(
            f"{module} timeout after {execution_time}s"
        )

        return {
            "error": f"{module} timeout"
        }

    except Exception as e:

        execution_time = round(
            time.time() - start_time,
            3
        )

        logger.error(
            f"{module} failed after {execution_time}s | {str(e)}"
        )

        return {
            "error": str(e)
        }


@router.post("/analyze")
def analyze(request: AnalyzeRequest):

    try:

        query = request.query.strip() if request.query else ""

        logger.info(f"Incoming query: {query}")

        if not query:

            return {
                "query": "",
                "agent": ["nlp"],
                "module_results": {},
                "status": "empty query"
            }

        # -----------------------------
        # AGENT DECISION
        # -----------------------------
        agent_result = run_agent(query)

        modules = []

        if isinstance(agent_result, str):

            modules = [agent_result]

        elif isinstance(agent_result, list):

            modules = agent_result

        elif isinstance(agent_result, dict):

            action = agent_result.get("action")

            if action:
                modules = [action]

        # fallback
        if not modules:
            modules = ["nlp"]

        logger.info(f"Selected modules: {modules}")

        # -----------------------------
        # EXECUTE MODULES
        # -----------------------------
        module_outputs = {}

        for module in modules:

            service = SERVICE_MAP.get(module)

            if service:

                module_outputs[module] = execute_with_timeout(
                    service,
                    query,
                    module
                )

            else:

                logger.error(f"{module} not implemented")

                module_outputs[module] = {
                    "error": "module not implemented"
                }

        return {

            "query": query,

            "agent": modules,

            "module_results": module_outputs,

            "status": "success"

        }

    except Exception as e:

        logger.error(f"Critical integration error | {str(e)}")

        return {

            "query": request.query,

            "agent": ["nlp"],

            "module_results": {

                "nlp": {

                    "error": "fallback response"

                }

            },

            "status": "error"

        }