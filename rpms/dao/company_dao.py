"""
CompanyDAO - Data Access Object for Company entity.
"""
from rpms.util.db_connection import get_connection
from rpms.model.company import Company


class CompanyDAO:

    def save(self, company: Company) -> int:
        """Insert a new company and return the generated ID."""
        sql = """
            INSERT INTO companies
            (company_name, industry, location, contact_person, contact_email, contact_phone, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (
                company.company_name, company.industry, company.location,
                company.contact_person, company.contact_email,
                company.contact_phone, company.status
            ))
            con.commit()
            return cursor.lastrowid
        finally:
            if con:
                con.close()

    def find_by_id(self, company_id: int) -> Company | None:
        """Find a company by primary key."""
        sql = "SELECT * FROM companies WHERE company_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (company_id,))
            row = cursor.fetchone()
            return self._map(row) if row else None
        finally:
            if con:
                con.close()

    def find_all(self) -> list[Company]:
        """Return all companies."""
        sql = "SELECT * FROM companies ORDER BY company_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def find_by_name(self, name: str) -> list[Company]:
        """Find companies by name (case-insensitive partial match)."""
        sql = "SELECT * FROM companies WHERE company_name LIKE %s ORDER BY company_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (f"%{name}%",))
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def update_status(self, company_id: int, status: str) -> bool:
        """Update the status of a company."""
        sql = "UPDATE companies SET status = %s WHERE company_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (status, company_id))
            con.commit()
            return cursor.rowcount > 0
        finally:
            if con:
                con.close()

    def update(self, company: Company) -> bool:
        """Update an existing company's details."""
        sql = """
            UPDATE companies SET
                company_name = %s, industry = %s, location = %s,
                contact_person = %s, contact_email = %s, contact_phone = %s, status = %s
            WHERE company_id = %s
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (
                company.company_name, company.industry, company.location,
                company.contact_person, company.contact_email,
                company.contact_phone, company.status, company.company_id
            ))
            con.commit()
            return cursor.rowcount > 0
        finally:
            if con:
                con.close()

    def _map(self, row: dict) -> Company:
        """Map a database row dict to a Company object."""
        return Company(
            company_id=row["company_id"],
            company_name=row["company_name"],
            industry=row.get("industry", ""),
            location=row.get("location", ""),
            contact_person=row.get("contact_person", ""),
            contact_email=row.get("contact_email", ""),
            contact_phone=row.get("contact_phone", ""),
            status=row["status"],
        )
