"""
JobDAO - Data Access Object for Job entity.
"""
from rpms.util.db_connection import get_connection
from rpms.model.job import Job


class JobDAO:

    def save(self, job: Job) -> int:
        """Insert a new job and return the generated ID."""
        sql = """
            INSERT INTO jobs
            (company_id, job_title, employment_type, location, openings,
             min_package_lpa, max_package_lpa, min_percentage,
             min_passing_year, max_passing_year, max_backlogs,
             posted_date, application_deadline, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (
                job.company_id, job.job_title, job.employment_type, job.location,
                job.openings, job.min_package_lpa, job.max_package_lpa,
                job.min_percentage, job.min_passing_year, job.max_passing_year,
                job.max_backlogs, job.posted_date, job.application_deadline, job.status
            ))
            con.commit()
            return cursor.lastrowid
        finally:
            if con:
                con.close()

    def find_by_id(self, job_id: int) -> Job | None:
        """Find a job by primary key."""
        sql = "SELECT * FROM jobs WHERE job_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (job_id,))
            row = cursor.fetchone()
            return self._map(row) if row else None
        finally:
            if con:
                con.close()

    def find_all(self) -> list[Job]:
        """Return all jobs."""
        sql = "SELECT * FROM jobs ORDER BY job_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def find_open_jobs(self) -> list[Job]:
        """Return all jobs with status OPEN."""
        sql = "SELECT * FROM jobs WHERE status = 'OPEN' ORDER BY job_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def find_by_company(self, company_id: int) -> list[Job]:
        """Return all jobs for a given company."""
        sql = "SELECT * FROM jobs WHERE company_id = %s ORDER BY job_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (company_id,))
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def find_by_title(self, title: str) -> list[Job]:
        """Return jobs matching title (partial, case-insensitive)."""
        sql = "SELECT * FROM jobs WHERE job_title LIKE %s ORDER BY job_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (f"%{title}%",))
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def close_job(self, job_id: int) -> bool:
        """Set a job's status to CLOSED."""
        sql = "UPDATE jobs SET status = 'CLOSED' WHERE job_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (job_id,))
            con.commit()
            return cursor.rowcount > 0
        finally:
            if con:
                con.close()

    def _map(self, row: dict) -> Job:
        """Map a database row dict to a Job object."""
        return Job(
            job_id=row["job_id"],
            company_id=row["company_id"],
            job_title=row["job_title"],
            employment_type=row.get("employment_type", ""),
            location=row.get("location", ""),
            openings=int(row.get("openings", 1)),
            min_package_lpa=float(row.get("min_package_lpa", 0)),
            max_package_lpa=float(row.get("max_package_lpa", 0)),
            min_percentage=float(row.get("min_percentage", 0)),
            min_passing_year=int(row.get("min_passing_year", 0)),
            max_passing_year=int(row.get("max_passing_year", 0)),
            max_backlogs=int(row.get("max_backlogs", 0)),
            posted_date=row.get("posted_date"),
            application_deadline=row.get("application_deadline"),
            status=row["status"],
        )
