import atexit
import json
import logging.config
import pathlib
import os

logger = logging.getLogger("ga4_app")  # __name__ is a common choice


def setup_logging():
    config_file = pathlib.Path("localserver/logfolder/logging_configs.json")
    with open(config_file) as f_in:
        config = json.load(f_in)

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)

    os.makedirs("localserver/logfolder/logs", exist_ok=True)
