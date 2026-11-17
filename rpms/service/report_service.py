"""
ReportService - Reporting and analytics service for recruitment management.
"""
from rpms.util.db_connection import get_connection


class ReportService:

    def candidate_count_by_technology(self) -> list[dict]:
        """Candidate count grouped by primary technology."""
        sql = """
            SELECT primary_technology, COUNT(*) AS count
            FROM candidates
            GROUP BY primary_technology
            ORDER BY count DESC
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            if con:
                con.close()

    def open_jobs_report(self) -> list[dict]:
        """List of all open jobs with company details."""
        sql = """
            SELECT j.job_id, j.job_title, c.company_name, j.location,
                   j.openings, j.min_package_lpa, j.max_package_lpa,
                   j.application_deadline
            FROM jobs j
            JOIN companies c ON j.company_id = c.company_id
            WHERE j.status = 'OPEN'
            ORDER BY j.job_id
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            if con:
                con.close()

    def applications_by_status(self) -> list[dict]:
        """Application counts grouped by status."""
        sql = """
            SELECT application_status, COUNT(*) AS count
            FROM applications
            GROUP BY application_status
            ORDER BY count DESC
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            if con:
                con.close()

    def company_wise_placements(self) -> list[dict]:
        """Placed candidate count per company."""
        sql = """
            SELECT c.company_name, COUNT(p.placement_id) AS placed_count
            FROM placements p
            JOIN offers o ON p.offer_id = o.offer_id
            JOIN applications a ON o.application_id = a.application_id
            JOIN jobs j ON a.job_id = j.job_id
            JOIN companies c ON j.company_id = c.company_id
            WHERE p.joining_status = 'JOINED'
            GROUP BY c.company_id, c.company_name
            ORDER BY placed_count DESC
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            if con:
                con.close()

    def placed_candidates(self) -> list[dict]:
        """List of candidates who have been successfully placed."""
        sql = """
            SELECT c.candidate_id, c.full_name, c.email, c.primary_technology,
                   p.actual_joining_date, o.designation, o.offered_package_lpa,
                   comp.company_name
            FROM placements p
            JOIN candidates c ON p.candidate_id = c.candidate_id
            JOIN offers o ON p.offer_id = o.offer_id
            JOIN applications a ON o.application_id = a.application_id
            JOIN jobs j ON a.job_id = j.job_id
            JOIN companies comp ON j.company_id = comp.company_id
            WHERE p.joining_status = 'JOINED'
            ORDER BY p.actual_joining_date DESC
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            if con:
                con.close()

    def unplaced_candidates(self) -> list[dict]:
        """List of active candidates who have not yet been placed."""
        sql = """
            SELECT candidate_id, full_name, email, mobile,
                   primary_technology, percentage, passing_year
            FROM candidates
            WHERE placement_status = 'UNPLACED' AND profile_status = 'ACTIVE'
            ORDER BY passing_year DESC, percentage DESC
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            if con:
                con.close()

    def pending_interviews(self) -> list[dict]:
        """List of upcoming/scheduled interviews."""
        sql = """
            SELECT i.interview_id, c.full_name AS candidate_name,
                   comp.company_name, j.job_title, i.round_number,
                   i.round_type, i.interview_date, i.mode, i.interviewer
            FROM interviews i
            JOIN applications a ON i.application_id = a.application_id
            JOIN candidates c ON a.candidate_id = c.candidate_id
            JOIN jobs j ON a.job_id = j.job_id
            JOIN companies comp ON j.company_id = comp.company_id
            WHERE i.interview_status = 'SCHEDULED'
            ORDER BY i.interview_date ASC
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            if con:
                con.close()

    def recruitment_funnel(self) -> dict[str, int]:
        """Recruitment funnel count across all key stages."""
        stages = [
            "APPLIED", "SHORTLISTED", "INTERVIEW_SCHEDULED",
            "INTERVIEWED", "SELECTED", "OFFERED", "JOINED", "REJECTED"
        ]
        sql = "SELECT application_status, COUNT(*) AS cnt FROM applications GROUP BY application_status"
        funnel = {stage: 0 for stage in stages}
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            for row in cursor.fetchall():
                status = row["application_status"]
                if status in funnel:
                    funnel[status] = row["cnt"]
            return funnel
        finally:
            if con:
                con.close()
