from sqlite3 import Error


class DatabaseRequests:
    def __init__(self, db) -> None:
        self.__db = db
        self.__cur = db.cursor()

    def add(self, userid: int, username: str, message: str, photo_id: str, video_id: str, time: str) -> bool:
        try:
            self.__cur.execute("INSERT INTO requests_table VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)", (userid, username, message, photo_id, video_id, time, '', ''))
            self.__db.commit()
            return True
        except Error as e:
            print(e)
            return False

    def update(self, request_id: int, msg: str, msg_time: str) -> bool:
        try:
            self.__cur.execute("UPDATE requests_table SET answer = ?, answer_time = ? WHERE ? = id", (msg, msg_time, request_id,))
            self.__db.commit()
            return True
        except Error as e:
            print(e)
            return False

    def get(self, request_id: int = None) -> list | None:
        try:
            if request_id is None:
                self.__cur.execute("SELECT * FROM requests_table ORDER BY id")
                return self.__cur.fetchall()
            else:
                self.__cur.execute("SELECT * FROM requests_table WHERE id = ?", (request_id,))
                return self.__cur.fetchone()
        except Error as e:
            print(e)
            return None

    def delete(self, request_id: int = None) -> bool:
        try:
            if request_id is None:
                self.__cur.execute("DELETE FROM requests_table")
            else:
                self.__cur.execute("DELETE FROM requests_table WHERE id == ?", (request_id,))
            self.__db.commit()
            return True
        except Error as e:
            print(e)
            return False
