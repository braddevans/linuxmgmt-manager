import json
import os


class ConfigManager:
    def __init__(self):
        self.config_file = "data/config.json"
        self.config = {}
        self.refresh_config()

    def get_config(self):
        return self.config

    def refresh_config(self):
        with open(self.config_file, "r") as f:
            self.config = json.load(f)
        pass
