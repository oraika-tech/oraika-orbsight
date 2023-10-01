import logging


def initialize_logger(name: str):
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)  # stop prefect verbose logging
    return logging.getLogger(name)
