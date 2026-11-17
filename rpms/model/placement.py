"""
Placement model using dataclass.
"""
from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Placement:
    placement_id: Optional[int] = None
    offer_id: int = 0
    candidate_id: int = 0
    actual_joining_date: Optional[date] = None
    joining_status: str = "JOINED"   # JOINED / NOT_JOINED / DEFERRED / NO_SHOW

    def __str__(self):
        return (
            f"[{self.placement_id}] Offer#{self.offer_id} | Candidate#{self.candidate_id} | "
            f"Joining Date: {self.actual_joining_date} | Status: {self.joining_status}"
        )
