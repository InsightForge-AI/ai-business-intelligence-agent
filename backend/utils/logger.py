"""
==========================================================
Logger
==========================================================

Application logger configuration.
"""

import logging


LOGGER_NAME = "DocuMind Backend"


logger = logging.getLogger(

    LOGGER_NAME

)

logger.setLevel(

    logging.INFO

)


if not logger.handlers:

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(message)s"

    )

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(

        formatter

    )

    logger.addHandler(

        console_handler

    )

    logger.propagate = False