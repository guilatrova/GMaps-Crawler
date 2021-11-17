from rich import inspect, print

from gmaps_crawler.entities import Place


class Storage:
    def save(self, place: Place):
        print(f"[yellow]{'=' * 100}[/yellow]")
        inspect(place)
        print(f"[yellow]{'=' * 100}[/yellow]")
