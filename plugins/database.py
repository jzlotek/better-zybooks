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

    def get_num_attempts(self, username, class_id, assignment_id) -> int:
        data = self.database.execute(
            """
            SELECT count(*) FROM assignments A, classes C, attempts At WHERE
            A.class = C.class AND At.assignment = A.assignment
            AND At.user = ? AND A.class = ? AND A.assignment = ?
            """,
            [username, class_id, assignment_id]
        ).fetchone()
        if data:
            return int(data[0])
        return 0

    def register_class(self, username, class_id):
        self.database.execute(
            """
            INSERT INTO registry (user, class)
            values (?, ?)
            """,
            [username, class_id]
        )

    def get_registered_classes(self, username) -> list:
        data = self.database.execute(
            """
            SELECT R.class, C.name FROM registry R
            INNER JOIN classes C ON C.class = R.class
            WHERE R.user = ?
            """,
            [username]
        ).fetchall()
        if data:
            return list(map(lambda x: {"class": x[0], "name": x[1]}, data))
        return []

    def get_assignments(self, class_id) -> list:
        data = self.database.execute(
            """SELECT assignment, class, name FROM assignments A WHERE A.class = ?""",
            [class_id]
        ).fetchall()
        if data:
            return list(map(lambda x: {"assignment": x[0], "class": x[1], "name": x[2]}, data))
        return []

    def get_classes(self) -> list:
        data = self.database.execute(
            """SELECT class, name FROM classes"""
        ).fetchall()
        if data:
            return list(map(lambda x: {"class": x[0], "name": x[1]}, data))
        return []

    def get_classes_not_registered(self, user) -> list:
        data = self.database.execute(
            """SELECT class, name FROM classes
            WHERE class NOT IN
            (SELECT class FROM registry WHERE user = ?)
            """,
            [user]
        ).fetchall()
        if data:
            return list(map(lambda x: {"class": x[0], "name": x[1]}, data))
        return []

    def get_class_info(self, class_id) -> list:
        data = self.database.execute(
            """SELECT class, name FROM classes WHERE class = ?""",
            [class_id]
        ).fetchone()
        if data:
            return {"class": data[0], "name": data[1]}
        return None

    def set_latest_attempt(self, username, assignment_id, data, score=0, maxscore=1):
        self.database.execute(
            """
            insert into attempts (user, assignment, data, score, attempt, maxscore)
            values (?, ?, ?, ?, null, ?)
            """,
            [username, assignment_id, data, score, maxscore]
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
