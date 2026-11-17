"""
Interview model using dataclass.
"""
from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Interview:
    interview_id: Optional[int] = None
    application_id: int = 0
    round_number: int = 1
    round_type: str = ""       # APTITUDE / TECHNICAL / MANAGERIAL / HR
    interview_date: Optional[date] = None
    mode: str = ""             # ONLINE / OFFLINE / TELEPHONIC
    interviewer: str = ""
    interview_status: str = "SCHEDULED"   # SCHEDULED / COMPLETED / CANCELLED

    def __str__(self):
        return (
            f"[{self.interview_id}] App#{self.application_id} | Round {self.round_number} "
            f"({self.round_type}) | Date: {self.interview_date} | Mode: {self.mode} | "
            f"Interviewer: {self.interviewer} | Status: {self.interview_status}"
        )


@dataclass
class InterviewFeedback:
    feedback_id: Optional[int] = None
    interview_id: int = 0
    technical_rating: float = 0.0
    communication_rating: float = 0.0
    problem_solving_rating: float = 0.0
    overall_rating: float = 0.0
    recommendation: str = ""   # NEXT_ROUND / SELECTED / REJECTED / ON_HOLD
    remarks: str = ""

    def __str__(self):
        return (
            f"[Feedback for Interview#{self.interview_id}] "
            f"Tech: {self.technical_rating} | Comm: {self.communication_rating} | "
            f"PS: {self.problem_solving_rating} | Overall: {self.overall_rating} | "
            f"Recommendation: {self.recommendation} | Remarks: {self.remarks}"
        )
