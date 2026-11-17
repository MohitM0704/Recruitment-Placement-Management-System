"""
InterviewDAO - Data Access Object for Interview and InterviewFeedback entities.
"""
from rpms.util.db_connection import get_connection
from rpms.model.interview import Interview, InterviewFeedback


class InterviewDAO:

    def save(self, interview: Interview) -> int:
        """Insert a new interview and return the generated ID."""
        sql = """
            INSERT INTO interviews
            (application_id, round_number, round_type, interview_date, mode, interviewer, interview_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (
                interview.application_id, interview.round_number, interview.round_type,
                interview.interview_date, interview.mode, interview.interviewer,
                interview.interview_status
            ))
            con.commit()
            return cursor.lastrowid
        finally:
            if con:
                con.close()

    def find_by_application(self, application_id: int) -> list[Interview]:
        """Return all interviews for a given application."""
        sql = "SELECT * FROM interviews WHERE application_id = %s ORDER BY round_number"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (application_id,))
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def find_by_id(self, interview_id: int) -> Interview | None:
        """Find an interview by primary key."""
        sql = "SELECT * FROM interviews WHERE interview_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (interview_id,))
            row = cursor.fetchone()
            return self._map(row) if row else None
        finally:
            if con:
                con.close()

    def update_status(self, interview_id: int, status: str) -> bool:
        """Update the status of an interview."""
        sql = "UPDATE interviews SET interview_status = %s WHERE interview_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (status, interview_id))
            con.commit()
            return cursor.rowcount > 0
        finally:
            if con:
                con.close()

    def save_feedback(self, feedback: InterviewFeedback) -> int:
        """Insert interview feedback and return the generated ID."""
        sql = """
            INSERT INTO interview_feedback
            (interview_id, technical_rating, communication_rating,
             problem_solving_rating, overall_rating, recommendation, remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (
                feedback.interview_id, feedback.technical_rating,
                feedback.communication_rating, feedback.problem_solving_rating,
                feedback.overall_rating, feedback.recommendation, feedback.remarks
            ))
            # Mark interview as COMPLETED when feedback is saved
            cursor2 = con.cursor()
            cursor2.execute(
                "UPDATE interviews SET interview_status = 'COMPLETED' WHERE interview_id = %s",
                (feedback.interview_id,)
            )
            con.commit()
            return cursor.lastrowid
        finally:
            if con:
                con.close()

    def find_feedback_by_interview(self, interview_id: int) -> InterviewFeedback | None:
        """Find feedback for a specific interview."""
        sql = "SELECT * FROM interview_feedback WHERE interview_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (interview_id,))
            row = cursor.fetchone()
            return self._map_feedback(row) if row else None
        finally:
            if con:
                con.close()

    def _map(self, row: dict) -> Interview:
        """Map a database row dict to an Interview object."""
        return Interview(
            interview_id=row["interview_id"],
            application_id=row["application_id"],
            round_number=int(row["round_number"]),
            round_type=row["round_type"],
            interview_date=row.get("interview_date"),
            mode=row.get("mode", ""),
            interviewer=row.get("interviewer", ""),
            interview_status=row["interview_status"],
        )

    def _map_feedback(self, row: dict) -> InterviewFeedback:
        """Map a database row dict to an InterviewFeedback object."""
        return InterviewFeedback(
            feedback_id=row["feedback_id"],
            interview_id=row["interview_id"],
            technical_rating=float(row.get("technical_rating", 0)),
            communication_rating=float(row.get("communication_rating", 0)),
            problem_solving_rating=float(row.get("problem_solving_rating", 0)),
            overall_rating=float(row.get("overall_rating", 0)),
            recommendation=row.get("recommendation", ""),
            remarks=row.get("remarks", ""),
        )
