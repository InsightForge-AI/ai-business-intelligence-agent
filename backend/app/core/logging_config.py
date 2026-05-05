import logging
import os

def setup_logging():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    LOG_DIR = os.path.join(BASE_DIR, "logs")

    os.makedirs(LOG_DIR, exist_ok=True)

    LOG_FILE = os.path.join(LOG_DIR, "app.log")
    ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")

    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


    # create handlers
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))


    error_handler = logging.FileHandler(ERROR_LOG_FILE, encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(log_format))


    # root logger
    root_logger = logging.getLogger()

    # remove existing handlers
    for h in root_logger.handlers[:]:
        root_logger.removeHandler(h)

    root_logger.setLevel(logging.INFO)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)


    # test entry
    root_logger.info("LOGGING WORKING")