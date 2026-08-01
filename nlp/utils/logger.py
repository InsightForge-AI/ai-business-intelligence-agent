"""
==========================================================
Logger
==========================================================

Responsibilities
----------------
• Configure application logging
"""

import logging


logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)


logger = logging.getLogger("nlp")