import yaml
from .logger import MyLogger

class YAMLHelper:
    def __init__(self, filename):
        self.logger = MyLogger("YAMLHelper")
        self.filename = filename
        self.load_yaml()
        self.check_necessary_keys(["API_KEY", "RSS", "INTERESTS"])

    def load_yaml(self):
        with open(self.filename, 'r') as file:
            self.data = yaml.safe_load(file)
            self.logger.info(f"Loaded YAML data from {self.filename}")

    def check_necessary_keys(self, required_keys):
        missing_keys = [key for key in required_keys if key not in self.data]
        if missing_keys:
            self.logger.error(f"Missing required keys in YAML: {missing_keys}")
            raise ValueError(f"Missing required keys in YAML: {missing_keys}")
        self.logger.info("All required keys are present in the YAML.")