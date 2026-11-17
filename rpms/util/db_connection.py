"""
Database connection utility for the RPMS application.
Connects to MySQL using mysql-connector-python.
"""
import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "recruitment_portal",
}


def get_connection():
    """
    Create and return a new MySQL database connection.
    Caller is responsible for closing the connection.
    """
    try:
        con = mysql.connector.connect(**DB_CONFIG)
        return con
    except Error as e:
        raise ConnectionError(f"Failed to connect to database: {e}")
