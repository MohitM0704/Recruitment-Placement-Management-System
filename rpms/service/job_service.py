"""
JobService - Business logic for job opening management.
"""
from rpms.dao.job_dao import JobDAO
from rpms.model.job import Job
from rpms.exception.exceptions import JobNotFoundError, CompanyNotFoundError
from rpms.dao.company_dao import CompanyDAO


class JobService:

    def __init__(self, job_dao: JobDAO | None = None, company_dao: CompanyDAO | None = None):
        self.job_dao = job_dao or JobDAO()
        self.company_dao = company_dao or CompanyDAO()

    def create_job(self, job: Job) -> int:
        """Validate and create a job opening."""
        if not job.job_title or not job.job_title.strip():
            raise ValueError("Job title cannot be empty.")

        if not job.company_id:
            raise ValueError("Company ID is required.")

        company = self.company_dao.find_by_id(job.company_id)
        if not company:
            raise CompanyNotFoundError(job.company_id)

        if job.openings <= 0:
            raise ValueError("Openings must be greater than zero.")

        if job.min_package_lpa < 0 or job.max_package_lpa < 0:
            raise ValueError("Package cannot be negative.")

        if job.min_package_lpa > job.max_package_lpa:
            raise ValueError("Minimum package cannot exceed maximum package.")

        if job.min_percentage < 0 or job.min_percentage > 100:
            raise ValueError("Percentage requirement must be between 0 and 100.")

        if job.max_backlogs < 0:
            raise ValueError("Allowed backlogs cannot be negative.")

        job.job_title = job.job_title.strip()
        return self.job_dao.save(job)

    def get_job(self, job_id: int) -> Job:
        """Find job by ID or raise JobNotFoundError."""
        job = self.job_dao.find_by_id(job_id)
        if not job:
            raise JobNotFoundError(job_id)
        return job

    def get_all_jobs(self) -> list[Job]:
        """Return all jobs."""
        return self.job_dao.find_all()

    def get_open_jobs(self) -> list[Job]:
        """Return all OPEN jobs."""
        return self.job_dao.find_open_jobs()

    def search_by_title(self, title: str) -> list[Job]:
        """Search jobs by title."""
        return self.job_dao.find_by_title(title.strip())

    def close_job(self, job_id: int) -> bool:
        """Close a job opening."""
        existing = self.job_dao.find_by_id(job_id)
        if not existing:
            raise JobNotFoundError(job_id)
        return self.job_dao.close_job(job_id)
