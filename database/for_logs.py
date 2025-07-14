from sqlite3 import Error


class DatabaseLogs:
    def __init__(self, db) -> None:
        self.__db = db
        self.__cur = db.cursor()

    def add(self, userid: int, username: str, message: str, time: int) -> bool:
        try:
            self.__cur.execute("INSERT INTO log VALUES(NULL, ?, ?, ?, ?)", (userid, username, message, time,))
            self.__db.commit()
            return True
        except Error as e:
            print(e)
            return False
