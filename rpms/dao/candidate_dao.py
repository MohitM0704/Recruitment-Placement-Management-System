"""
CandidateDAO - Data Access Object for Candidate entity.
"""
from rpms.util.db_connection import get_connection
from rpms.model.candidate import Candidate


class CandidateDAO:

    def save(self, candidate: Candidate) -> int:
        """Insert a new candidate and return the generated ID."""
        sql = """
            INSERT INTO candidates
            (full_name, email, mobile, primary_technology, skills, percentage,
             passing_year, backlog_count, profile_status, placement_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (
                candidate.full_name, candidate.email, candidate.mobile,
                candidate.primary_technology, candidate.skills, candidate.percentage,
                candidate.passing_year, candidate.backlog_count,
                candidate.profile_status, candidate.placement_status
            ))
            con.commit()
            return cursor.lastrowid
        finally:
            if con:
                con.close()

    def find_by_id(self, candidate_id: int) -> Candidate | None:
        """Find a candidate by primary key."""
        sql = "SELECT * FROM candidates WHERE candidate_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (candidate_id,))
            row = cursor.fetchone()
            return self._map(row) if row else None
        finally:
            if con:
                con.close()

    def find_all(self) -> list[Candidate]:
        """Return all candidates."""
        sql = "SELECT * FROM candidates ORDER BY candidate_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def find_by_email(self, email: str) -> Candidate | None:
        """Find a candidate by email address."""
        sql = "SELECT * FROM candidates WHERE email = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (email,))
            row = cursor.fetchone()
            return self._map(row) if row else None
        finally:
            if con:
                con.close()

    def find_by_mobile(self, mobile: str) -> Candidate | None:
        """Find a candidate by mobile number."""
        sql = "SELECT * FROM candidates WHERE mobile = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (mobile,))
            row = cursor.fetchone()
            return self._map(row) if row else None
        finally:
            if con:
                con.close()

    def find_by_technology(self, technology: str) -> list[Candidate]:
        """Find candidates by primary technology (case-insensitive partial match)."""
        sql = "SELECT * FROM candidates WHERE primary_technology LIKE %s ORDER BY candidate_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (f"%{technology}%",))
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def find_by_name(self, name: str) -> list[Candidate]:
        """Find candidates by full name (case-insensitive partial match)."""
        sql = "SELECT * FROM candidates WHERE full_name LIKE %s ORDER BY candidate_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (f"%{name}%",))
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def update(self, candidate: Candidate) -> bool:
        """Update an existing candidate's details."""
        sql = """
            UPDATE candidates SET
                full_name = %s, email = %s, mobile = %s,
                primary_technology = %s, skills = %s, percentage = %s,
                passing_year = %s, backlog_count = %s, profile_status = %s
            WHERE candidate_id = %s
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (
                candidate.full_name, candidate.email, candidate.mobile,
                candidate.primary_technology, candidate.skills, candidate.percentage,
                candidate.passing_year, candidate.backlog_count,
                candidate.profile_status, candidate.candidate_id
            ))
            con.commit()
            return cursor.rowcount > 0
        finally:
            if con:
                con.close()

    def deactivate(self, candidate_id: int) -> bool:
        """Set a candidate's profile_status to INACTIVE."""
        sql = "UPDATE candidates SET profile_status = 'INACTIVE' WHERE candidate_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (candidate_id,))
            con.commit()
            return cursor.rowcount > 0
        finally:
            if con:
                con.close()

    def update_placement_status(self, candidate_id: int, placement_status: str) -> bool:
        """Update the placement status of a candidate."""
        sql = "UPDATE candidates SET placement_status = %s WHERE candidate_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (placement_status, candidate_id))
            con.commit()
            return cursor.rowcount > 0
        finally:
            if con:
                con.close()

    def _map(self, row: dict) -> Candidate:
        """Map a database row dict to a Candidate object."""
        return Candidate(
            candidate_id=row["candidate_id"],
            full_name=row["full_name"],
            email=row["email"],
            mobile=row["mobile"],
            primary_technology=row["primary_technology"],
            skills=row.get("skills", ""),
            percentage=float(row["percentage"]),
            passing_year=int(row["passing_year"]),
            backlog_count=int(row["backlog_count"]),
            profile_status=row["profile_status"],
            placement_status=row["placement_status"],
        )
