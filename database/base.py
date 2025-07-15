from sqlite3 import Error

class BaseDatabase:
    def __init__(self, db) -> None:
        self.db = db
        self.cur = db.cursor()

class Table(BaseDatabase):
    def __init__(self, db, table_name, columns):
        super().__init__(db)
        self.table_name = table_name
        self.columns = columns

    def insert(self, values):
        placeholders = ', '.join(['?'] * len(values))
        sql = f"INSERT INTO {self.table_name} ({', '.join(self.columns)}) VALUES ({placeholders})"
        try:
            self.cur.execute(sql, values)
            self.db.commit()
            return True
        except Error as e:
            print(e)
            return False

    def delete(self, id: int = None) -> bool:
        if id is None:
            sql = f"DELETE FROM {self.table_name}"
            try:
                self.cur.execute(sql)
                self.db.commit()
                return True
            except Error as e:
                print(e)
                return False
        else:
            sql = f"DELETE FROM {self.table_name} WHERE id = ?"
            try:
                self.cur.execute(sql, (id,))
                self.db.commit()
                return True
            except Error as e:
                print(e)
                return False

    def select(self, condition=None, params=None):
        sql = f"SELECT * FROM {self.table_name}"
        if condition:
            sql += f" WHERE {condition}"
        try:
            if params:
                self.cur.execute(sql, params)
                return self.cur.fetchone() if condition else self.cur.fetchall()
            else:
                self.cur.execute(sql)
                return self.cur.fetchall()
        except Error as e:
            print(e)
            return None

    def update(self, set_clause, condition, params):
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {condition}"
        try:
            self.cur.execute(sql, params)
            self.db.commit()
            return True
        except Error as e:
            print(e)
            return False

class DatabaseLogs(Table):
    def __init__(self, db):
        super().__init__(db, "log", ["userid", "username", "message", "time"])

    def add(self, userid: int, username: str, message: str, time: int) -> bool:
        return self.insert((userid, username, message, time))

class DatabaseQuestions(Table):
    def __init__(self, db):
        super().__init__(db, "questions", ["question", "answer"])

    def add(self, text: str, answer: str) -> bool:
        return self.insert((text, answer))

    def delete(self, question_id: int = None) -> bool:
        return super().delete(question_id)

    def get(self, question_id: int = None) -> list | None:
        if question_id is None:
            return super().select()
        return super().select("id = ?", (question_id,))

class DatabaseRequests(Table):
    def __init__(self, db):
        super().__init__(db, "requests_table", ["userid", "username", "message", "photo_id", "video_id", "time", "answer", "answer_time"])

    def add(self, userid: int, username: str, message: str, photo_id: str, video_id: str, time: str) -> bool:
        return self.insert((userid, username, message, photo_id, video_id, time, '', ''))

    def update(self, request_id: int, msg: str, msg_time: str) -> bool:
        return super().update("answer = ?, answer_time = ?", "id = ?", (msg, msg_time, request_id))

    def get(self, request_id: int = None) -> list | None:
        if request_id is None:
            return super().select()
        return super().select("id = ?", (request_id,))

    def delete(self, request_id: int = None) -> bool:
        return super().delete(request_id)