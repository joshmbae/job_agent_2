"""Job listing sources used by the agent."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Protocol

import json


@dataclass
class JobListing:
    """Simple representation of a job posting."""

    company: str
    title: str
    description: str
    url: str

    @property
    def keywords(self) -> List[str]:
        text = f"{self.title} {self.description}".lower()
        tokens = {token.strip(".,:;!?") for token in text.split() if token}
        return sorted(token for token in tokens if len(token) > 2)


class JobSource(Protocol):
    """Interface for job sources."""

    def get_job_listings(self) -> Iterable[JobListing]:
        ...


class LocalJobSource:
    """Loads job listings from a JSON file on disk."""

    def __init__(self, json_path: str | Path) -> None:
        self.json_path = Path(json_path)

    def get_job_listings(self) -> Iterable[JobListing]:
        with self.json_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        for raw in data:
            yield JobListing(
                company=raw["company"],
                title=raw["title"],
                description=raw["description"],
                url=raw["url"],
            )
