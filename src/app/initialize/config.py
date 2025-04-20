import os
from dotenv import load_dotenv


class EnvLoader:
    def __init__(self, env_file=".env"):
        load_dotenv(env_file, override=True)
        self.env_vars = {key: os.getenv(key) for key in os.environ.keys()}

        self.URL = self.get("URL")
        self.OS = self.get("OS")
        self.USERNAME = self.get("USERNAME")
        self.PASSWORD = self.get("PASSWORD")
        self.MATRIX = self.get_matrix("MATRIX")

    def get(self, key, default=None):
        return self.env_vars.get(key, default)

    def get_matrix(self, key):
        value = self.get(key)
        if value:
            return [list(map(str, row.split(","))) for row in value.split(";")]
        return None
