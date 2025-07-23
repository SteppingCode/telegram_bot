from os import path
from sqlite3 import connect, Connection, Row
from database.base import DatabaseLogs, DatabaseRequests, DatabaseQuestions


class DatabaseManager:
    def __init__(self):
        self.db = self.connect_db()
        self.logs = DatabaseLogs(self.db)
        self.requests = DatabaseRequests(self.db)
        self.questions = DatabaseQuestions(self.db)

    @staticmethod
    def connect_db() -> Connection:
        """
        Connect to the database and set up the schema if necessary.
        :return: Connection to the database
        """
        conn = connect(path.join("database", "database.db"))
        conn.row_factory = Row
        cur = conn.cursor()
        with open(path.join("database", "script.sql"), 'r') as scheme:
            cur.executescript(scheme.read())
        return conn


# Single instance of DatabaseManager
db_manager = DatabaseManager()
