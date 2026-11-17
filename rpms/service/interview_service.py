"""
InterviewService - Business logic for scheduling interviews and recording feedback.
"""
from rpms.dao.interview_dao import InterviewDAO
from rpms.dao.application_dao import ApplicationDAO
from rpms.model.interview import Interview, InterviewFeedback
from rpms.exception.exceptions import (
    InterviewNotFoundError,
    ApplicationNotFoundError,
)


class InterviewService:

    def __init__(
        self,
        interview_dao: InterviewDAO | None = None,
        application_dao: ApplicationDAO | None = None,
    ):
        self.interview_dao = interview_dao or InterviewDAO()
        self.application_dao = application_dao or ApplicationDAO()

    def schedule_interview(self, interview: Interview) -> int:
        """Schedule a new interview round for an application."""
        if not interview.application_id:
            raise ValueError("Application ID is required.")

        app = self.application_dao.find_by_id(interview.application_id)
        if not app:
            raise ApplicationNotFoundError(interview.application_id)

        if interview.round_number < 1:
            raise ValueError("Round number must be 1 or higher.")

        # Update application status to INTERVIEW_SCHEDULED
        self.application_dao.update_status(interview.application_id, "INTERVIEW_SCHEDULED")

        return self.interview_dao.save(interview)

    def get_interview(self, interview_id: int) -> Interview:
        """Find interview by ID or raise InterviewNotFoundError."""
        interview = self.interview_dao.find_by_id(interview_id)
        if not interview:
            raise InterviewNotFoundError(interview_id)
        return interview

    def get_by_application(self, application_id: int) -> list[Interview]:
        """Return all interview rounds for an application."""
        return self.interview_dao.find_by_application(application_id)

    def update_interview_status(self, interview_id: int, status: str) -> bool:
        """Update interview status (SCHEDULED/COMPLETED/CANCELLED)."""
        existing = self.interview_dao.find_by_id(interview_id)
        if not existing:
            raise InterviewNotFoundError(interview_id)
        return self.interview_dao.update_status(interview_id, status.strip().upper())

    def add_feedback(self, feedback: InterviewFeedback) -> int:
        """
        Record feedback for an interview round.
        Also transitions application to INTERVIEWED or SELECTED / REJECTED.
        """
        if not feedback.interview_id:
            raise ValueError("Interview ID is required.")

        interview = self.interview_dao.find_by_id(feedback.interview_id)
        if not interview:
            raise InterviewNotFoundError(feedback.interview_id)

        # Validate rating ranges
        for field, name in [
            (feedback.technical_rating, "Technical"),
            (feedback.communication_rating, "Communication"),
            (feedback.problem_solving_rating, "Problem Solving"),
            (feedback.overall_rating, "Overall"),
        ]:
            if field < 0 or field > 5:
                raise ValueError(f"{name} rating must be between 0 and 5.")

        feedback_id = self.interview_dao.save_feedback(feedback)

        # Update application status based on recommendation
        rec = feedback.recommendation.upper()
        if rec == "SELECTED":
            self.application_dao.update_status(interview.application_id, "SELECTED")
        elif rec == "REJECTED":
            self.application_dao.update_status(interview.application_id, "REJECTED")
        else:
            self.application_dao.update_status(interview.application_id, "INTERVIEWED")

        return feedback_id

    def get_feedback(self, interview_id: int) -> InterviewFeedback | None:
        """Get feedback for an interview round."""
        return self.interview_dao.find_feedback_by_interview(interview_id)
