"""
CandidateService - Business logic for candidate operations.
"""
from rpms.dao.candidate_dao import CandidateDAO
from rpms.model.candidate import Candidate
from rpms.exception.exceptions import CandidateNotFoundError
from rpms.util.validation import (
    is_valid_email,
    is_valid_mobile,
    is_valid_percentage,
    is_valid_backlog_count,
)


class CandidateService:

    def __init__(self, candidate_dao: CandidateDAO | None = None):
        self.candidate_dao = candidate_dao or CandidateDAO()

    def add_candidate(self, candidate: Candidate) -> int:
        """Validate candidate details and save to database."""
        if not candidate.full_name or not candidate.full_name.strip():
            raise ValueError("Candidate name cannot be empty.")

        if not is_valid_email(candidate.email):
            raise ValueError(f"Invalid email address: '{candidate.email}'.")

        if not is_valid_mobile(candidate.mobile):
            raise ValueError("Mobile number must be exactly 10 digits.")

        if not is_valid_percentage(candidate.percentage):
            raise ValueError("Percentage must be between 0 and 100.")

        if not is_valid_backlog_count(candidate.backlog_count):
            raise ValueError("Backlog count cannot be negative.")

        if self.candidate_dao.find_by_email(candidate.email.strip()):
            raise ValueError(f"Candidate with email '{candidate.email}' already exists.")

        if self.candidate_dao.find_by_mobile(candidate.mobile.strip()):
            raise ValueError(f"Candidate with mobile '{candidate.mobile}' already exists.")

        candidate.email = candidate.email.strip()
        candidate.mobile = candidate.mobile.strip()
        candidate.full_name = candidate.full_name.strip()
        return self.candidate_dao.save(candidate)

    def get_candidate(self, candidate_id: int) -> Candidate:
        """Retrieve a candidate by ID or raise CandidateNotFoundError."""
        candidate = self.candidate_dao.find_by_id(candidate_id)
        if not candidate:
            raise CandidateNotFoundError(candidate_id)
        return candidate

    def get_all_candidates(self) -> list[Candidate]:
        """Return all candidates."""
        return self.candidate_dao.find_all()

    def search_by_name(self, name: str) -> list[Candidate]:
        """Search candidates by name."""
        return self.candidate_dao.find_by_name(name.strip())

    def search_by_technology(self, technology: str) -> list[Candidate]:
        """Search candidates by primary technology."""
        return self.candidate_dao.find_by_technology(technology.strip())

    def update_candidate(self, candidate: Candidate) -> bool:
        """Update candidate details."""
        if not candidate.candidate_id:
            raise ValueError("Candidate ID required for update.")

        existing = self.candidate_dao.find_by_id(candidate.candidate_id)
        if not existing:
            raise CandidateNotFoundError(candidate.candidate_id)

        if not is_valid_email(candidate.email):
            raise ValueError(f"Invalid email: '{candidate.email}'.")

        if not is_valid_mobile(candidate.mobile):
            raise ValueError("Mobile number must be exactly 10 digits.")

        if not is_valid_percentage(candidate.percentage):
            raise ValueError("Percentage must be between 0 and 100.")

        if not is_valid_backlog_count(candidate.backlog_count):
            raise ValueError("Backlog count cannot be negative.")

        # Check unique constraints if changed
        email_owner = self.candidate_dao.find_by_email(candidate.email.strip())
        if email_owner and email_owner.candidate_id != candidate.candidate_id:
            raise ValueError(f"Email '{candidate.email}' is in use by another candidate.")

        mobile_owner = self.candidate_dao.find_by_mobile(candidate.mobile.strip())
        if mobile_owner and mobile_owner.candidate_id != candidate.candidate_id:
            raise ValueError(f"Mobile '{candidate.mobile}' is in use by another candidate.")

        return self.candidate_dao.update(candidate)

    def deactivate_candidate(self, candidate_id: int) -> bool:
        """Deactivate candidate profile (soft delete)."""
        existing = self.candidate_dao.find_by_id(candidate_id)
        if not existing:
            raise CandidateNotFoundError(candidate_id)
        return self.candidate_dao.deactivate(candidate_id)
