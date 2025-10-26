"""Utilities for logging job applications."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, TypedDict

import csv


class ApplicationRecord(TypedDict):
    timestamp: str
    company: str
    title: str
    url: str
    candidate_name: str
    candidate_email: str
    resume_path: str


@dataclass
class ApplicationTracker:
    """Persist job application attempts to a CSV file."""

    output_path: Path

    def __init__(self, output_path: str | Path) -> None:
        self.output_path = Path(output_path)
        if not self.output_path.exists():
            self.output_path.write_text("timestamp,company,title,url,candidate_name,candidate_email,resume_path\n")

    def record_application(
        self,
        *,
        company: str,
        title: str,
        url: str,
        candidate_name: str,
        candidate_email: str,
        resume_path: str,
    ) -> ApplicationRecord:
        record = ApplicationRecord(
            timestamp=datetime.utcnow().isoformat(timespec="seconds"),
            company=company,
            title=title,
            url=url,
            candidate_name=candidate_name,
            candidate_email=candidate_email,
            resume_path=resume_path,
        )
        with self.output_path.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(record.keys()))
            writer.writerow(record)
        return record

    def iter_applications(self) -> Iterable[ApplicationRecord]:
        with self.output_path.open("r", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                yield ApplicationRecord(**row)

    def list_applications(self) -> List[ApplicationRecord]:
        return list(self.iter_applications())
