"""
ApplicationDAO - Data Access Object for Application entity.
"""
from rpms.util.db_connection import get_connection
from rpms.model.application import Application


class ApplicationDAO:

    def save(self, application: Application) -> int:
        """Insert a new application and return the generated ID."""
        sql = """
            INSERT INTO applications
            (candidate_id, job_id, application_date, application_status,
             eligibility_status, eligibility_reason)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (
                application.candidate_id, application.job_id,
                application.application_date, application.application_status,
                application.eligibility_status, application.eligibility_reason
            ))
            con.commit()
            return cursor.lastrowid
        finally:
            if con:
                con.close()

    def exists(self, candidate_id: int, job_id: int) -> bool:
        """Return True if the candidate has already applied for the job."""
        sql = "SELECT 1 FROM applications WHERE candidate_id = %s AND job_id = %s LIMIT 1"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (candidate_id, job_id))
            return cursor.fetchone() is not None
        finally:
            if con:
                con.close()

    def find_by_candidate(self, candidate_id: int) -> list[Application]:
        """Return all applications for a given candidate."""
        sql = "SELECT * FROM applications WHERE candidate_id = %s ORDER BY application_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (candidate_id,))
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def find_by_job(self, job_id: int) -> list[Application]:
        """Return all applications for a given job."""
        sql = "SELECT * FROM applications WHERE job_id = %s ORDER BY application_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (job_id,))
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def find_by_id(self, application_id: int) -> Application | None:
        """Find an application by primary key."""
        sql = "SELECT * FROM applications WHERE application_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (application_id,))
            row = cursor.fetchone()
            return self._map(row) if row else None
        finally:
            if con:
                con.close()

    def update_status(self, application_id: int, status: str) -> bool:
        """Update the status of an application."""
        sql = "UPDATE applications SET application_status = %s WHERE application_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (status, application_id))
            con.commit()
            return cursor.rowcount > 0
        finally:
            if con:
                con.close()

    def find_all(self) -> list[Application]:
        """Return all applications."""
        sql = "SELECT * FROM applications ORDER BY application_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def _map(self, row: dict) -> Application:
        """Map a database row dict to an Application object."""
        return Application(
            application_id=row["application_id"],
            candidate_id=row["candidate_id"],
            job_id=row["job_id"],
            application_date=row.get("application_date"),
            application_status=row["application_status"],
            eligibility_status=row.get("eligibility_status", "ELIGIBLE"),
            eligibility_reason=row.get("eligibility_reason", ""),
        )
