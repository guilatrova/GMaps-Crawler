class GMapsCrawlerException(Exception):
    pass


class MissingEnvVariable(GMapsCrawlerException):
    def __init__(self, env_var: str) -> None:
        message = f"Missing env variable: '{env_var}'"
        super().__init__(message)
