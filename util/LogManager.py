import logging
from logging.handlers import RotatingFileHandler

from util.ConfigManager import ConfigManager

config_manager = ConfigManager()
config = config_manager.get_config()


class LogManager:
    def __init__(self):
        self.log = None

    def create_rotating_log(self):
        """
        Creates a rotating log
        """
        logger = logging.getLogger("Rotating Log")
        logger.setLevel(logging.INFO)

        log_format = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', "%Y-%m-%d %H:%M:%S")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_format)
        stream_handler.setLevel(logging.INFO)
        logger.addHandler(stream_handler)

        # add a rotating handler
        # max size of 2MB, backup count of 5
        rotating_log_handler = RotatingFileHandler(config["logs"]["directory"] + "main.log", maxBytes=2000000, backupCount=5)
        rotating_log_handler.setFormatter(log_format)
        logger.addHandler(rotating_log_handler)

        self.log = logger

    def get_log(self):
        if self.log is None:
            # print("Log not created yet")
            # print(f"Log directory: {config['logs']['directory']}")
            # print(f"log: {self.log}")
            self.create_rotating_log()
        return self.log

    def log_message(self, prefix, message):
        """
        Logs a message
        """
        self.get_log().info(f"[{prefix}]: " + message)
