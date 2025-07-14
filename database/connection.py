from os import path
from sqlite3 import connect, Connection, Row
from database.for_requests import DatabaseRequests
from database.for_logs import DatabaseLogs
from database.for_questions import DatabaseQuestions


def connect_db(db_name: str) -> Connection:
    """
    Connect to the database
    :return connection: Connection to the database
    """
    conn = connect(path.join("extra", f"{db_name}.db"))
    conn.row_factory = Row
    cur = conn.cursor()
    with open(path.join("database", f"{db_name}.sql"), 'r') as scheme:
        cur.execute(scheme.read())
    return conn


def logs_db() -> DatabaseLogs:
    db = connect_db(db_name='logging')
    database = DatabaseLogs(db)
    return database


def requests_db() -> DatabaseRequests:
    db = connect_db(db_name='requests')
    database = DatabaseRequests(db)
    return database


def questions_db() -> DatabaseQuestions:
    db = connect_db(db_name='questions')
    database = DatabaseQuestions(db)
    return database
