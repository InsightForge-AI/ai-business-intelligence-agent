"""
==========================================================
Agent Constants
==========================================================

Configuration values used across
the Agent service.
"""

# ---------------------------------------------------------
# Service Information
# ---------------------------------------------------------

MODULE_NAME = "agent"

SERVICE_NAME = "DocuMind Agent Service"

VERSION = "1.0.0"

# ---------------------------------------------------------
# Ollama Configuration
# ---------------------------------------------------------

MODEL_NAME = "phi3:latest"

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

DEFAULT_TIMEOUT = 300

# ---------------------------------------------------------
# Supported Modules
# ---------------------------------------------------------

AVAILABLE_MODULES = [

    "ml",

    "nlp",

    "rag",

    "cv"

]

# ---------------------------------------------------------
# Supported Intents
# ---------------------------------------------------------

INTENTS = [

    "business_analysis",

    "document_summary",

    "question_answering",

    "data_analysis",

    "document_extraction",

    "chart_analysis",

    "general_query"

]

# ---------------------------------------------------------
# Default Execution Order
# ---------------------------------------------------------

EXECUTION_ORDER = {

    "business_analysis": [

        "rag",

        "ml",

        "nlp"

    ],

    "document_summary": [

        "rag",

        "nlp"

    ],

    "question_answering": [

        "rag"

    ],

    "data_analysis": [

        "ml"

    ],

    "document_extraction": [

        "cv",

        "rag"

    ],

    "chart_analysis": [

        "cv",

        "ml"

    ],

    "general_query": [

        "rag"

    ]

}