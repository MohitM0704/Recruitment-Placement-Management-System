"""
EligibilityService - Automated eligibility check engine.
"""
from datetime import date
from rpms.model.candidate import Candidate
from rpms.model.job import Job


class EligibilityService:

    def check_eligibility(self, candidate: Candidate, job: Job) -> tuple[bool, str]:
        """
        Evaluate candidate against job criteria.
        Returns (is_eligible: bool, reason: str).
        """
        reasons = []

        # 1. Candidate profile status
        if candidate.profile_status.upper() != "ACTIVE":
            reasons.append("Candidate profile is not ACTIVE")

        # 2. Job status
        if job.status.upper() != "OPEN":
            reasons.append(f"Job is not OPEN (status: {job.status})")

        # 3. Application deadline
        if job.application_deadline:
            if date.today() > job.application_deadline:
                reasons.append(f"Application deadline has passed ({job.application_deadline})")

        # 4. Percentage requirement
        if job.min_percentage and candidate.percentage < job.min_percentage:
            reasons.append(
                f"Candidate percentage ({candidate.percentage}%) is below minimum required ({job.min_percentage}%)"
            )

        # 5. Passing year requirements
        if job.min_passing_year and candidate.passing_year < job.min_passing_year:
            reasons.append(
                f"Passing year ({candidate.passing_year}) is earlier than required minimum ({job.min_passing_year})"
            )

        if job.max_passing_year and candidate.passing_year > job.max_passing_year:
            reasons.append(
                f"Passing year ({candidate.passing_year}) exceeds required maximum ({job.max_passing_year})"
            )

        # 6. Backlog criteria
        if candidate.backlog_count > job.max_backlogs:
            reasons.append(
                f"Candidate backlogs ({candidate.backlog_count}) exceed allowed maximum ({job.max_backlogs})"
            )

        if reasons:
            return False, "; ".join(reasons)
        return True, "Meets all eligibility criteria"
