from sqlite3 import Error


class DatabaseQuestions:
    def __init__(self, db) -> None:
        self.__db = db
        self.__cur = db.cursor()

    def add(self, text: str, answer: str) -> bool:
        try:
            self.__cur.execute('INSERT INTO questions VALUES (NULL, ?, ?)', (text, answer,))
            self.__db.commit()
            return True
        except Error as e:
            print(e)
            return False

    def delete(self, question_id: int = None) -> bool:
        try:
            if question_id is None:
                self.__cur.execute('DELETE FROM questions')
            else:
                self.__cur.execute('DELETE FROM questions WHERE id == ?', (question_id,))
            self.__db.commit()
            return True
        except Error as e:
            print(e)
            return False

    def get(self, question_id: int = None) -> list | None:
        try:
            if question_id is None:
                self.__cur.execute('SELECT * FROM questions ORDER BY id')
                return self.__cur.fetchall()
            else:
                self.__cur.execute('SELECT * FROM questions WHERE id == ?', (question_id,))
                return self.__cur.fetchone()
        except Error as e:
            print(e)
            return None