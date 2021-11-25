from abc import ABC, abstractclassmethod

from rich import inspect, print

from gmaps_crawler.config import StorageMode, settings
from gmaps_crawler.entities import Place


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
    def save(self, place: Place):
        return super().save(place)


def get_storage() -> BaseStorage:
    if settings.STORAGE_MODE == StorageMode.DEBUG:
        return DebugStorage()

    if settings.STORAGE_MODE == StorageMode.SQS:
        return SqsStorage()

    raise ValueError(f"{settings.STORAGE_MODE} is unknown")
