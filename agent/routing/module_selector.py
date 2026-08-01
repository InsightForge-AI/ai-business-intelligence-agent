"""
==========================================================
Module Selector
==========================================================

Responsibilities
----------------
• Select AI modules based on intent
• Adjust modules based on file type
• Return execution modules
"""

from utils.constants import EXECUTION_ORDER


def select_modules(
    intent: str,
    metadata: dict
) -> list[str]:
    """
    Select modules for execution.
    """

    # --------------------------------------------------
    # Default Modules
    # --------------------------------------------------

    modules = list(

        EXECUTION_ORDER.get(

            intent,

            ["rag"]

        )

    )

    # --------------------------------------------------
    # File Type
    # --------------------------------------------------

    file_type = (

        metadata.get(

            "file_type",

            ""

        )

        .lower()

        .lstrip(".")

    )

    # --------------------------------------------------
    # Image Documents
    # --------------------------------------------------

    if file_type in [

        "jpg",

        "jpeg",

        "png",

        "bmp",

        "tiff"

    ]:

        modules = [

            module

            for module in modules

            if module != "ml"

        ]

        if "cv" not in modules:

            modules.insert(

                0,

                "cv"

            )

    # --------------------------------------------------
    # PDF
    # --------------------------------------------------

    elif file_type == "pdf":

        if "rag" not in modules:

            modules.append(

                "rag"

            )

        if "cv" not in modules:

            modules.insert(

                0,

                "cv"

            )

    # --------------------------------------------------
    # Word / Text Documents
    # --------------------------------------------------

    elif file_type in [

        "doc",

        "docx",

        "txt"

    ]:

        modules = [

            module

            for module in modules

            if module != "cv"

        ]

        if "nlp" not in modules:

            modules.insert(

                0,

                "nlp"

            )

        if "rag" not in modules:

            modules.append(

                "rag"

            )

    # --------------------------------------------------
    # Structured Data
    # --------------------------------------------------

    elif file_type in [

        "csv",

        "xlsx",

        "xls"

    ]:

        modules = [

            module

            for module in modules

            if module != "cv"

        ]

        if "ml" not in modules:

            modules.insert(

                0,

                "ml"

            )

    # --------------------------------------------------
    # Remove Duplicates
    # --------------------------------------------------

    modules = list(

        dict.fromkeys(

            modules

        )

    )

    return modules