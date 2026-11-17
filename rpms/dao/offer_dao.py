"""
OfferDAO - Data Access Object for Offer entity.
"""
from rpms.util.db_connection import get_connection
from rpms.model.offer import Offer


class OfferDAO:

    def save(self, offer: Offer) -> int:
        """Insert a new offer and return the generated ID."""
        sql = """
            INSERT INTO offers
            (application_id, designation, offered_package_lpa,
             offer_date, expected_joining_date, offer_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (
                offer.application_id, offer.designation, offer.offered_package_lpa,
                offer.offer_date, offer.expected_joining_date, offer.offer_status
            ))
            con.commit()
            return cursor.lastrowid
        finally:
            if con:
                con.close()

    def find_by_application(self, application_id: int) -> list[Offer]:
        """Return all offers for a given application."""
        sql = "SELECT * FROM offers WHERE application_id = %s ORDER BY offer_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (application_id,))
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def find_by_id(self, offer_id: int) -> Offer | None:
        """Find an offer by primary key."""
        sql = "SELECT * FROM offers WHERE offer_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (offer_id,))
            row = cursor.fetchone()
            return self._map(row) if row else None
        finally:
            if con:
                con.close()

    def update_status(self, offer_id: int, status: str) -> bool:
        """Update the status of an offer."""
        sql = "UPDATE offers SET offer_status = %s WHERE offer_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (status, offer_id))
            con.commit()
            return cursor.rowcount > 0
        finally:
            if con:
                con.close()

    def find_all(self) -> list[Offer]:
        """Return all offers."""
        sql = "SELECT * FROM offers ORDER BY offer_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def _map(self, row: dict) -> Offer:
        """Map a database row dict to an Offer object."""
        return Offer(
            offer_id=row["offer_id"],
            application_id=row["application_id"],
            designation=row.get("designation", ""),
            offered_package_lpa=float(row.get("offered_package_lpa", 0)),
            offer_date=row.get("offer_date"),
            expected_joining_date=row.get("expected_joining_date"),
            offer_status=row["offer_status"],
        )
