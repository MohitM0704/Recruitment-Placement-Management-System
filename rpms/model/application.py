"""
Application model using dataclass.
"""
from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Application:
    application_id: Optional[int] = None
    candidate_id: int = 0
    job_id: int = 0
    application_date: Optional[date] = None
    application_status: str = "APPLIED"   # APPLIED/SHORTLISTED/INTERVIEW_SCHEDULED/INTERVIEWED/SELECTED/OFFERED/JOINED/REJECTED
    eligibility_status: str = "ELIGIBLE"  # ELIGIBLE / NOT_ELIGIBLE
    eligibility_reason: str = ""

    def __str__(self):
        return (
            f"[{self.application_id}] Candidate#{self.candidate_id} → Job#{self.job_id} | "
            f"Date: {self.application_date} | Status: {self.application_status} | "
            f"Eligibility: {self.eligibility_status} ({self.eligibility_reason})"
        )
