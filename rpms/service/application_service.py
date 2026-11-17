"""
ApplicationService - Business logic for job applications and workflow transitions.
"""
from datetime import date
from rpms.dao.application_dao import ApplicationDAO
from rpms.dao.candidate_dao import CandidateDAO
from rpms.dao.job_dao import JobDAO
from rpms.model.application import Application
from rpms.service.eligibility_service import EligibilityService
from rpms.exception.exceptions import (
    CandidateNotFoundError,
    JobNotFoundError,
    ApplicationNotFoundError,
    DuplicateApplicationError,
    CandidateNotEligibleError,
    InvalidStatusTransitionError,
)

# Valid workflow forward and alternate transitions
VALID_TRANSITIONS = {
    "APPLIED": ["SHORTLISTED", "REJECTED"],
    "SHORTLISTED": ["INTERVIEW_SCHEDULED", "REJECTED"],
    "INTERVIEW_SCHEDULED": ["INTERVIEWED", "REJECTED"],
    "INTERVIEWED": ["SELECTED", "REJECTED", "INTERVIEW_SCHEDULED"],
    "SELECTED": ["OFFERED", "REJECTED"],
    "OFFERED": ["JOINED", "REJECTED"],
    "JOINED": [],
    "REJECTED": [],
}


class ApplicationService:

    def __init__(
        self,
        application_dao: ApplicationDAO | None = None,
        candidate_dao: CandidateDAO | None = None,
        job_dao: JobDAO | None = None,
        eligibility_service: EligibilityService | None = None,
    ):
        self.application_dao = application_dao or ApplicationDAO()
        self.candidate_dao = candidate_dao or CandidateDAO()
        self.job_dao = job_dao or JobDAO()
        self.eligibility_service = eligibility_service or EligibilityService()

    def apply_for_job(self, candidate_id: int, job_id: int) -> int:
        """
        Validate candidate, job, check duplicate application,
        verify eligibility, and save application.
        """
        candidate = self.candidate_dao.find_by_id(candidate_id)
        if not candidate:
            raise CandidateNotFoundError(candidate_id)

        job = self.job_dao.find_by_id(job_id)
        if not job:
            raise JobNotFoundError(job_id)

        # Check duplicate
        if self.application_dao.exists(candidate_id, job_id):
            raise DuplicateApplicationError(candidate_id, job_id)

        # Eligibility check
        is_eligible, reason = self.eligibility_service.check_eligibility(candidate, job)
        if not is_eligible:
            raise CandidateNotEligibleError(reason)

        application = Application(
            candidate_id=candidate_id,
            job_id=job_id,
            application_date=date.today(),
            application_status="APPLIED",
            eligibility_status="ELIGIBLE",
            eligibility_reason=reason,
        )

        return self.application_dao.save(application)

    def get_application(self, application_id: int) -> Application:
        """Find application by ID or raise ApplicationNotFoundError."""
        app = self.application_dao.find_by_id(application_id)
        if not app:
            raise ApplicationNotFoundError(application_id)
        return app

    def get_all_applications(self) -> list[Application]:
        """Return all applications."""
        return self.application_dao.find_all()

    def get_by_candidate(self, candidate_id: int) -> list[Application]:
        """Get all applications for candidate."""
        return self.application_dao.find_by_candidate(candidate_id)

    def get_by_job(self, job_id: int) -> list[Application]:
        """Get all applications for job."""
        return self.application_dao.find_by_job(job_id)

    def update_status(self, application_id: int, target_status: str) -> bool:
        """
        Update application workflow status with transition validation.
        """
        app = self.get_application(application_id)
        current = app.application_status.upper()
        target = target_status.strip().upper()

        allowed = VALID_TRANSITIONS.get(current, [])
        if target not in allowed:
            raise InvalidStatusTransitionError(current, target)

        return self.application_dao.update_status(application_id, target)
