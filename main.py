"""Command line interface for the job application agent."""

from __future__ import annotations

import argparse

from job_agent import ApplicationTracker, CandidateProfile, JobApplicationAgent, LocalJobSource


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Match jobs and record applications automatically.")
    parser.add_argument("description", help="Keywords that describe the desired job", nargs="+")
    parser.add_argument("--jobs", default="data/jobs.json", help="Path to job listings JSON")
    parser.add_argument("--log", default="applications.csv", help="CSV file to log applications")
    parser.add_argument("--name", required=True, help="Candidate full name")
    parser.add_argument("--email", required=True, help="Candidate email address")
    parser.add_argument("--resume", required=True, help="Path to resume file")
    parser.add_argument("--threshold", type=float, default=0.4, help="Keyword match threshold")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    job_source = LocalJobSource(args.jobs)
    tracker = ApplicationTracker(args.log)
    candidate = CandidateProfile(name=args.name, email=args.email, resume_path=args.resume)
    agent = JobApplicationAgent(
        job_source=job_source,
        tracker=tracker,
        candidate=candidate,
        keyword_threshold=args.threshold,
    )

    matches = agent.apply_to_matches(args.description)

    if matches:
        print("Submitted applications for the following positions:")
        for match in matches:
            print(f"- {match.listing.title} at {match.listing.company} (score: {match.score:.2f})")
    else:
        print("No matching positions found. No applications submitted.")


if __name__ == "__main__":
    main()
