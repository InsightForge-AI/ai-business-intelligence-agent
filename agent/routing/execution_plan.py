"""
==========================================================
Execution Planner
==========================================================

Responsibilities
----------------
• Build execution plan
• Order selected AI modules
• Return execution sequence
"""

from utils.constants import EXECUTION_ORDER


def build_execution_plan(
    intent: str,
    selected_modules: list[str]
) -> list[str]:
    """
    Build execution order.

    Parameters
    ----------
    intent : str

    selected_modules : list[str]

    Returns
    -------
    list[str]
    """

    # --------------------------------------------------
    # Default Order
    # --------------------------------------------------

    default_order = EXECUTION_ORDER.get(

        intent,

        ["rag"]

    )

    execution_order = []

    # --------------------------------------------------
    # Preserve Default Order
    # --------------------------------------------------

    for module in default_order:

        if module in selected_modules:

            execution_order.append(

                module

            )

    # --------------------------------------------------
    # Append Remaining Modules
    # --------------------------------------------------

    for module in selected_modules:

        if module not in execution_order:

            execution_order.append(

                module

            )

    return execution_order