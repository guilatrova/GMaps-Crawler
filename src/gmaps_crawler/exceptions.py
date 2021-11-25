from gmaps_crawler.entities import Place


class GMapsCrawlerException(Exception):
    pass


class MissingEnvVariable(GMapsCrawlerException):
    def __init__(self, env_var: str) -> None:
        message = f"Missing env variable: '{env_var}'"
        super().__init__(message)


class CantEmitPlace(GMapsCrawlerException):
    def __init__(self, place: Place, url: str) -> None:
        msg = f"Place {place} couldn't be emitted to SQS URL: {url}"
        super().__init__(msg)
