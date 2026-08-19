"""
==========================================================
Agent Service
==========================================================

Responsibilities
----------------
• Understand the user request
• Detect intent
• Select AI modules
• Generate execution plan
• Return standardized response
"""

from routing.intent_detector import detect_intent
from routing.module_selector import select_modules
from routing.execution_plan import build_execution_plan


async def run_agent(
    query: str,
    metadata: dict
) -> dict:
    """
    Execute the Agent workflow.

    Parameters
    ----------
    query : str

    metadata : dict

    Returns
    -------
    dict
    """

    # -----------------------------------------------------
    # Intent Detection
    # -----------------------------------------------------

    intent = await detect_intent(

        query=query,

        metadata=metadata

    )

    # -----------------------------------------------------
    # Module Selection
    # -----------------------------------------------------

    selected_modules = select_modules(

        intent=intent,

        metadata=metadata

    )

    # -----------------------------------------------------
    # Execution Plan
    # -----------------------------------------------------

    execution_order = build_execution_plan(

        intent=intent,

        selected_modules=selected_modules

    )

    # -----------------------------------------------------
    # Reason
    # -----------------------------------------------------

    reason = (

        f"The query was classified as "

        f"'{intent}', therefore the modules "

        f"{', '.join(selected_modules)} "

        f"will be executed."

    )

    # -----------------------------------------------------
    # Response
    # -----------------------------------------------------

    return {

        "module": "agent",

        "success": True,

        "intent": intent,

        "selected_modules": selected_modules,

        "execution_order": execution_order,

        "reason": reason,

        "message": "Execution plan generated successfully."

    }