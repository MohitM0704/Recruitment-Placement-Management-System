"""
Job model using dataclass.
"""
from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Job:
    job_id: Optional[int] = None
    company_id: int = 0
    job_title: str = ""
    employment_type: str = ""       # FULL_TIME / PART_TIME / CONTRACT / INTERNSHIP
    location: str = ""
    openings: int = 1
    min_package_lpa: float = 0.0
    max_package_lpa: float = 0.0
    min_percentage: float = 0.0
    min_passing_year: int = 0
    max_passing_year: int = 0
    max_backlogs: int = 0
    posted_date: Optional[date] = None
    application_deadline: Optional[date] = None
    status: str = "OPEN"            # OPEN / CLOSED / ON_HOLD

    def __str__(self):
        return (
            f"[{self.job_id}] {self.job_title} @ Company#{self.company_id} | "
            f"{self.employment_type} | {self.location} | Openings: {self.openings} | "
            f"Package: {self.min_package_lpa}-{self.max_package_lpa} LPA | "
            f"Min%: {self.min_percentage} | Yr: {self.min_passing_year}-{self.max_passing_year} | "
            f"Max Backlogs: {self.max_backlogs} | Deadline: {self.application_deadline} | Status: {self.status}"
        )
