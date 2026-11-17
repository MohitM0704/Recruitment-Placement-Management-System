"""
Candidate model using dataclass.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Candidate:
    candidate_id: Optional[int] = None
    full_name: str = ""
    email: str = ""
    mobile: str = ""
    primary_technology: str = ""
    skills: str = ""
    percentage: float = 0.0
    passing_year: int = 0
    backlog_count: int = 0
    profile_status: str = "ACTIVE"       # ACTIVE / INACTIVE
    placement_status: str = "UNPLACED"   # UNPLACED / PLACED

    def __str__(self):
        return (
            f"[{self.candidate_id}] {self.full_name} | {self.email} | {self.mobile} | "
            f"Tech: {self.primary_technology} | {self.percentage}% | "
            f"Yr: {self.passing_year} | Backlogs: {self.backlog_count} | "
            f"Status: {self.profile_status} | Placement: {self.placement_status}"
        )
