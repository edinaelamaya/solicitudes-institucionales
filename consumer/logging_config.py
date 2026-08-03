import logging
import os
import sys

import structlog


def configure_logging(log_level: str = "INFO", log_file_path: str = "/logs/consumer.jsonl") -> None:
    os.makedirs("/logs", exist_ok=True)
    file_handler = logging.FileHandler(log_file_path)
    stream_handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(format="%(message)s", handlers=[stream_handler, file_handler], level=log_level)
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, log_level.upper(), logging.INFO)),
        cache_logger_on_first_use=True,
    )
