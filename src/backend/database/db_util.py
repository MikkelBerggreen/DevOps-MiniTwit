from contextlib import contextmanager
from dotenv import dotenv_values
import psycopg2

dotenv = dotenv_values(".env")

class Database:

    @contextmanager
    def connect_db(self):
        connection = psycopg2.connect(
            host=dotenv["POSTGRES_SERVER"],
            database=dotenv["POSTGRES_DB"],
            user=dotenv["POSTGRES_USER"],
            password=dotenv["POSTGRES_PASSWORD"],
            port=dotenv["POSTGRES_PORT"],
        )

        try:
            yield connection
        finally:
            connection.close()

    def query_db(self, query, args=(), one=False):
        """Queries the database and returns a list of dictionaries."""
        with self.connect_db() as db:
            cur = db.cursor()
            cur.execute(query, args)
            rv = [
                dict((cur.description[idx][0], value) for idx, value in enumerate(row))
                for row in cur.fetchall()
            ]

            return (rv[0] if rv else None) if one else rv

    def insert_in_db(self, query, args=()):
        """Queries the database and returns a list of dictionaries."""
        with self.connect_db() as db:
            cur = db.cursor()
            cur.execute(query, args)
            db.commit()
            return cur.lastrowid

    def update_in_db(self, query, args=()):
        """Queries the database and returns a list of dictionaries."""
        db = self.connect_db()
        cur = db.cursor()
        cur.execute(query, args)
        db.commit()
        return cur.rowcount

    def get_user_id(self, username):
        """Convenience method to look up the id for a username."""
        with self.connect_db() as db:
            cur = db.cursor()
            cur.execute("select user_id from users where username = %s", [username])
            rv = cur.fetchall()
            return rv[0][0] if rv else None

    def execute_db(self, query, args=()):
        with self.connect_db() as db:
            cur = db.cursor()
            cur.execute(query, args)
            db.commit()
