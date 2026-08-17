from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
import concurrent.futures
import logging
import time

from config import REQUEST_TIMEOUT
from app.services.cv_service import run_cv
from app.services.agent_service import run_agent
from app.services.ml_service import run_ml
from app.services.nlp_service import run_nlp
from app.services.rag_service import run_rag


router = APIRouter()

logger = logging.getLogger(__name__)


class AnalyzeRequest(BaseModel):
    query: str
    # Populated by the frontend when the user attaches an image (sent as
    # base64 since the endpoint accepts a JSON body, not multipart). Both
    # must be present for the CV module to actually receive image bytes.
    file_name: Optional[str] = None
    file_data: Optional[str] = None


TIMEOUT = REQUEST_TIMEOUT


def execute_with_timeout(service, module):

    start_time = time.time()
    # Not used as a context manager: ThreadPoolExecutor.__exit__ calls
    # shutdown(wait=True), which blocks until the submitted task actually
    # finishes -- even after future.result(timeout=...) has already given
    # up waiting. That silently turned this "timeout" into a no-op for
    # slow/hung downstream calls. shutdown(wait=False) below lets the
    # response return on schedule regardless of how long the background
    # call takes; the outbound requests.post() calls now also carry their
    # own timeout= (see backend/app/services/*.py), so the abandoned
    # thread still terminates on its own shortly after.
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    try:
        future = executor.submit(service)
        result = future.result(timeout=TIMEOUT)

        execution_time = round(time.time() - start_time, 3)
        logger.info(f"{module} executed in {execution_time}s")
        return result

    except concurrent.futures.TimeoutError:
        execution_time = round(time.time() - start_time, 3)
        logger.error(f"{module} timeout after {execution_time}s")
        return {
            "error": f"{module} timeout"
        }

    except Exception as e:
        execution_time = round(time.time() - start_time, 3)
        logger.error(f"{module} failed after {execution_time}s | {str(e)}")
        return {
            "error": str(e)
        }

    finally:
        executor.shutdown(wait=False)


@router.post("/analyze")
def analyze(request: AnalyzeRequest):

    try:
        query = request.query.strip() if request.query else ""
        logger.info(f"Query: {query}")

        # agent decision
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

        if not modules:
            modules = ["nlp"]

        logger.info(f"Module selected: {modules}")

        service_map = {
            "nlp": lambda: run_nlp(query),
            "ml": lambda: run_ml(query),
            "rag": lambda: run_rag(query),
            "cv": lambda: run_cv(request.file_name, request.file_data),
        }

        module_outputs = {}

        for module in modules:
            service = service_map.get(module)

            if service:
                module_outputs[module] = execute_with_timeout(service, module)
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
        logger.error(f"Critical error | {str(e)}")
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
