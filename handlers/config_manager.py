import json


class ConfigManager:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfigManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, name_config_file: str = "config.json"):
        self.name_config_file = name_config_file
        self.configs = self.open_configs()

    def open_configs(self):
        try:
            with open(self.name_config_file, "r") as file:
                self.configs = json.load(file)
                return self.configs
        except FileNotFoundError:
            with open(self.name_config_file, "w") as file:
                json.dump({}, file)
                return {}

    def edit_config(self, name: str, value: str):
        self.configs[name] = value
        with open(self.name_config_file, "w", encoding="utf-8") as file:
            json.dump(self.configs, file)
