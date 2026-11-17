"""
Custom exceptions for the RPMS application.
"""


class RPMSBaseException(Exception):
    """Base exception for RPMS."""
    pass


class CandidateNotFoundError(RPMSBaseException):
    """Raised when a candidate cannot be found."""
    def __init__(self, identifier=None):
        message = f"Candidate not found: {identifier}" if identifier else "Candidate not found."
        super().__init__(message)


class JobNotFoundError(RPMSBaseException):
    """Raised when a job cannot be found."""
    def __init__(self, identifier=None):
        message = f"Job not found: {identifier}" if identifier else "Job not found."
        super().__init__(message)


class CompanyNotFoundError(RPMSBaseException):
    """Raised when a company cannot be found."""
    def __init__(self, identifier=None):
        message = f"Company not found: {identifier}" if identifier else "Company not found."
        super().__init__(message)


class DuplicateApplicationError(RPMSBaseException):
    """Raised when a candidate attempts to apply to a job they have already applied to."""
    def __init__(self, candidate_id=None, job_id=None):
        if candidate_id and job_id:
            message = f"Candidate {candidate_id} has already applied for job {job_id}."
        else:
            message = "Duplicate application detected."
        super().__init__(message)


class CandidateNotEligibleError(RPMSBaseException):
    """Raised when a candidate is not eligible for a job."""
    def __init__(self, reason=None):
        message = f"Candidate is not eligible: {reason}" if reason else "Candidate is not eligible."
        super().__init__(message)


class ApplicationNotFoundError(RPMSBaseException):
    """Raised when an application cannot be found."""
    def __init__(self, identifier=None):
        message = f"Application not found: {identifier}" if identifier else "Application not found."
        super().__init__(message)


class InterviewNotFoundError(RPMSBaseException):
    """Raised when an interview cannot be found."""
    def __init__(self, identifier=None):
        message = f"Interview not found: {identifier}" if identifier else "Interview not found."
        super().__init__(message)


class OfferNotFoundError(RPMSBaseException):
    """Raised when an offer cannot be found."""
    def __init__(self, identifier=None):
        message = f"Offer not found: {identifier}" if identifier else "Offer not found."
        super().__init__(message)


class PlacementNotFoundError(RPMSBaseException):
    """Raised when a placement cannot be found."""
    def __init__(self, identifier=None):
        message = f"Placement not found: {identifier}" if identifier else "Placement not found."
        super().__init__(message)


class InvalidStatusTransitionError(RPMSBaseException):
    """Raised when an invalid workflow status transition is attempted."""
    def __init__(self, current_status=None, target_status=None):
        if current_status and target_status:
            message = f"Cannot transition from '{current_status}' to '{target_status}'."
        else:
            message = "Invalid status transition."
        super().__init__(message)
