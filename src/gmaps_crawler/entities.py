from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Place:
    name: str
    address: str
    business_hours: dict[str, str] = field(default_factory=lambda: {})
    photo_link: Optional[str] = None
    rate: Optional[str] = None
    reviews: Optional[str] = None
    extra_attrs: dict[str, str] = field(default_factory=lambda: {})
    traits: dict[str, list[str]] = field(default_factory=lambda: {})

    @property
    def identifier(self) -> str:
        return ""
