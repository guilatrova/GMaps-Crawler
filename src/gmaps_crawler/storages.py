from abc import ABC, abstractclassmethod

from rich import inspect, print

from gmaps_crawler.config import settings
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


def get_storage() -> BaseStorage:
    if settings.STORAGE_MODE.upper() == "DEBUG":
        return DebugStorage()

    raise ValueError(f"{settings.STORAGE_MODE} is unknown")
