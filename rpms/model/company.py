"""
Company model using dataclass.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Company:
    company_id: Optional[int] = None
    company_name: str = ""
    industry: str = ""
    location: str = ""
    contact_person: str = ""
    contact_email: str = ""
    contact_phone: str = ""
    status: str = "ACTIVE"   # ACTIVE / INACTIVE / BLACKLISTED

    def __str__(self):
        return (
            f"[{self.company_id}] {self.company_name} | Industry: {self.industry} | "
            f"Location: {self.location} | Contact: {self.contact_person} ({self.contact_email}) | "
            f"Status: {self.status}"
        )
