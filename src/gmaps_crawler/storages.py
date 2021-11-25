from abc import ABC, abstractclassmethod

from rich import inspect, print

from gmaps_crawler.config import StorageMode, settings
from gmaps_crawler.entities import Place
from gmaps_crawler.exceptions import MissingEnvVariable
from gmaps_crawler.facades import SQSEmitter


class BaseStorage(ABC):
    @abstractclassmethod
    def save(self, place: Place):
        ...


class DebugStorage(BaseStorage):
    def save(self, place: Place):
        print(f"[yellow]{'=' * 100}[/yellow]")
        inspect(place)
        print(f"[yellow]{'=' * 100}[/yellow]")


class SqsStorage(BaseStorage):
    def __init__(self) -> None:
        if not settings.SCRAPED_EVENT_SQS_URL:
            raise MissingEnvVariable("SCRAPED_EVENT_SQS_URL")

        self.emitter = SQSEmitter(settings.SCRAPED_EVENT_SQS_URL)

    def save(self, place: Place):
        self.emitter.emit(place)


def get_storage() -> BaseStorage:
    if settings.STORAGE_MODE == StorageMode.DEBUG:
        return DebugStorage()

    if settings.STORAGE_MODE == StorageMode.SQS:
        return SqsStorage()

    raise ValueError(f"{settings.STORAGE_MODE} is unknown")
