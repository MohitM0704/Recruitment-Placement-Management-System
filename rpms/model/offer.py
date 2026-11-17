"""
Offer model using dataclass.
"""
from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Offer:
    offer_id: Optional[int] = None
    application_id: int = 0
    designation: str = ""
    offered_package_lpa: float = 0.0
    offer_date: Optional[date] = None
    expected_joining_date: Optional[date] = None
    offer_status: str = "OFFERED"   # OFFERED / ACCEPTED / REJECTED / EXPIRED / WITHDRAWN

    def __str__(self):
        return (
            f"[{self.offer_id}] App#{self.application_id} | {self.designation} | "
            f"Package: {self.offered_package_lpa} LPA | Offer Date: {self.offer_date} | "
            f"Expected Joining: {self.expected_joining_date} | Status: {self.offer_status}"
        )
