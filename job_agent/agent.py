"""Core automation logic for job applications."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .sources import JobListing, JobSource
from .tracker import ApplicationTracker


@dataclass
class CandidateProfile:
    """Simple container for candidate data used in applications."""

    name: str
    email: str
    resume_path: str
    cover_letter_template: str | None = None


@dataclass
class MatchResult:
    """Holds information about a job match."""

    listing: JobListing
    score: float
    matched_keywords: Sequence[str]


class JobApplicationAgent:
    """Match job descriptions and submit applications automatically."""

    def __init__(
        self,
        *,
        job_source: JobSource,
        tracker: ApplicationTracker,
        candidate: CandidateProfile,
        keyword_threshold: float = 0.4,
    ) -> None:
        self.job_source = job_source
        self.tracker = tracker
        self.candidate = candidate
        self.keyword_threshold = keyword_threshold

    def find_matches(self, desired_keywords: Iterable[str]) -> List[MatchResult]:
        """Return job listings whose keyword score exceeds the threshold."""

        keywords = {keyword.lower() for keyword in desired_keywords if keyword}
        matches: List[MatchResult] = []
        for listing in self.job_source.get_job_listings():
            score, matched = self._score_listing(listing, keywords)
            if score >= self.keyword_threshold:
                matches.append(MatchResult(listing=listing, score=score, matched_keywords=matched))
        matches.sort(key=lambda result: result.score, reverse=True)
        return matches

    def apply_to_matches(self, desired_keywords: Iterable[str]) -> List[MatchResult]:
        """Submit applications to all matching jobs and log the results."""

        matches = self.find_matches(desired_keywords)
        for match in matches:
            self._submit_application(match.listing)
        return matches

    def _score_listing(self, listing: JobListing, keywords: set[str]) -> tuple[float, List[str]]:
        """Score a listing based on how many keywords appear."""

        found = [keyword for keyword in keywords if keyword in listing.keywords]
        score = len(found) / len(keywords) if keywords else 0.0
        return score, found

    def _submit_application(self, listing: JobListing) -> None:
        """Record an application. Real integrations would live here."""

        self.tracker.record_application(
            company=listing.company,
            title=listing.title,
            url=listing.url,
            candidate_name=self.candidate.name,
            candidate_email=self.candidate.email,
            resume_path=self.candidate.resume_path,
        )

        # Stub for future implementation of sending emails or API requests.
        # For now, we simply record the application in the tracker.
