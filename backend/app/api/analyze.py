from fastapi import APIRouter
from pydantic import BaseModel
import concurrent.futures
import logging

from app.services.cv_service import run_cv
from app.services.agent_service import run_agent
from app.services.ml_service import run_ml
from app.services.nlp_service import run_nlp
from app.services.rag_service import run_rag


router = APIRouter()


# logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalyzeRequest(BaseModel):
    query: str


SERVICE_MAP = {

    "nlp": run_nlp,
    "ml": run_ml,
    "rag": run_rag,
    "cv": run_cv

}


TIMEOUT = 5


def execute_with_timeout(service, query, module):

    try:

        logger.info(f"Running module: {module}")

        with concurrent.futures.ThreadPoolExecutor() as executor:

            future = executor.submit(service, query)

            result = future.result(timeout=TIMEOUT)

            logger.info(f"{module} completed successfully")

            return result


    except concurrent.futures.TimeoutError:

        logger.error(f"{module} timeout")

        return {

            "error": f"{module} timeout"

        }


    except Exception as e:

        logger.error(f"{module} failed: {str(e)}")

        return {

            "error": str(e)

        }


@router.post("/analyze")

def analyze(request: AnalyzeRequest):

    try:

        query = request.query.strip() if request.query else ""

        logger.info(f"Received query: {query}")


        # call agent
        agent_result = run_agent(query)

        logger.info(f"Agent result: {agent_result}")


        # normalize agent output
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


        logger.info(f"Modules selected: {modules}")


        module_outputs = {}


        # run modules
        for module in modules:

            service = SERVICE_MAP.get(module)


            if service:

                module_outputs[module] = execute_with_timeout(

                    service,
                    query,
                    module

                )

            else:

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

        logger.error(f"Critical error: {str(e)}")

        return {

            "query": request.query,

            "agent": ["nlp"],

            "module_results": {

                "nlp": {

                    "error": "fallback response"

                }

            },

            "status": "error",

            "details": str(e)

        }
