import os
from SessionHandler import ThreadedTCPRequestHandler, ProcessTCPServer
import logging
from db import create_table


HOST, PORT = "0.0.0.0", 1337


def configure_logging():
    # Configure the logger
    LOG_LEVEL = os.getenv("LOG_LEVEL", "ERROR").upper()
    numeric_level = getattr(logging, LOG_LEVEL, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {LOG_LEVEL}")
    logging.basicConfig(filename="jigsaw.log", level=numeric_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logging.getLogger().addHandler(console_handler)


if __name__ == "__main__":
    configure_logging()
    create_table()
    logging.info(f"Starting jigsaw2 server ({HOST}:{PORT})")

    server = ProcessTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.serve_forever()
