"""Job application automation package."""

from .agent import CandidateProfile, JobApplicationAgent
from .tracker import ApplicationTracker
from .sources import LocalJobSource

__all__ = [
    "CandidateProfile",
    "JobApplicationAgent",
    "ApplicationTracker",
    "LocalJobSource",
]
