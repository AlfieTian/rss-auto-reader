import yaml
from logging import getLogger

class YAMLHelper:
    def __init__(self, filename):
        self.filename = filename
        self.load_yaml()
        self.check_necessary_keys(["OPENAI_API_KEY", "RSS", "Interests"])

    def load_yaml(self):
        with open(self.filename, 'r') as file:
            self.data = yaml.safe_load(file)
            logger = getLogger(__name__)
            logger.debug(f"Loaded YAML data from {self.filename}")

    def check_necessary_keys(self, required_keys):
        logger = getLogger(__name__)
        missing_keys = [key for key in required_keys if key not in self.data]
        if missing_keys:
            logger.error(f"Missing required keys in YAML: {missing_keys}")
            raise ValueError(f"Missing required keys in YAML: {missing_keys}")
        logger.debug("All required keys are present in the YAML.")