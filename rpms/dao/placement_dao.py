"""
PlacementDAO - Data Access Object for Placement entity.
"""
from rpms.util.db_connection import get_connection
from rpms.model.placement import Placement


class PlacementDAO:

    def save(self, placement: Placement) -> int:
        """Insert a new placement and return the generated ID."""
        sql = """
            INSERT INTO placements
            (offer_id, candidate_id, actual_joining_date, joining_status)
            VALUES (%s, %s, %s, %s)
        """
        con = None
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(sql, (
                placement.offer_id, placement.candidate_id,
                placement.actual_joining_date, placement.joining_status
            ))
            con.commit()
            return cursor.lastrowid
        finally:
            if con:
                con.close()

    def find_by_candidate(self, candidate_id: int) -> list[Placement]:
        """Return all placements for a given candidate."""
        sql = "SELECT * FROM placements WHERE candidate_id = %s ORDER BY placement_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (candidate_id,))
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def find_all_joined(self) -> list[Placement]:
        """Return all placements where joining_status is JOINED."""
        sql = "SELECT * FROM placements WHERE joining_status = 'JOINED' ORDER BY placement_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def find_all(self) -> list[Placement]:
        """Return all placements."""
        sql = "SELECT * FROM placements ORDER BY placement_id"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            return [self._map(r) for r in cursor.fetchall()]
        finally:
            if con:
                con.close()

    def find_by_id(self, placement_id: int) -> Placement | None:
        """Find a placement by primary key."""
        sql = "SELECT * FROM placements WHERE placement_id = %s"
        con = None
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (placement_id,))
            row = cursor.fetchone()
            return self._map(row) if row else None
        finally:
            if con:
                con.close()

    def _map(self, row: dict) -> Placement:
        """Map a database row dict to a Placement object."""
        return Placement(
            placement_id=row["placement_id"],
            offer_id=row["offer_id"],
            candidate_id=row["candidate_id"],
            actual_joining_date=row.get("actual_joining_date"),
            joining_status=row["joining_status"],
        )
