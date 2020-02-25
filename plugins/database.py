import json
import os
import sqlite3
import loguru

logger = loguru.logger


class Database(object):
    def __init__(self, dbpath='database.sqlite'):
        self.database = sqlite3.connect(os.path.abspath(dbpath))

    def execute(self, string, params=[]):
        return self.database.execute(string, params)

    def get_user(self, username):
        data = self.database.execute(
            f'SELECT username, password, name FROM users WHERE username=?', [str(username)]).fetchone()
        if data:
            return {
                'username': data[0],
                'password': data[1],
                'name': data[2]
            }
        return None


    def create_user(self, username, password, name):
        self.database.execute(f'INSERT INTO users (username, password, name) VALUES (?, ?, ?);',
                              [username, password, name])
        self.database.commit()


    def get_latest_attempt(self, username, class_id, assignment_id):
        data = self.database.execute(
            """
            SELECT At.data, At.attempt FROM assignments A, classes C, attempts At WHERE
            A.class = C.class AND At.assignment = A.assignment
            AND At.user = ? AND A.class = ? AND A.assignment = ?
            AND At.attempt >= (
                SELECT MAX(Atp.attempt) FROM attempts Atp WHERE 
                Atp.user = At.user AND Atp.assignment = At.assignment
            )
            """,
            [username, class_id, assignment_id]
        ).fetchone()
        if data:
            return json.loads(data[0])
        return {}
    

    def set_latest_attempt(self, username, assignment_id, data, score=0):
        self.database.execute(
            """
            insert into attempts (user, assignment, data, score, attempt)
            values (?, ?, ?, ?, null)
            """,
            [username, assignment_id, data, score]
        )
        self.database.commit()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        try:
            self.database.commit()
            self.database.close()
        except:
            pass

    def __del__(self):
        try:
            self.database.commit()
            self.database.close()
        except:
            pass
