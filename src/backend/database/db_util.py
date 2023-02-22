import sqlite3
from contextlib import closing
from dotenv import dotenv_values
dotenv = dotenv_values('.env')


def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(dotenv["DATABASE_URL"])


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    db = connect_db()
    cur = db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def insert_in_db(query, args=()):
    """Queries the database and returns a list of dictionaries."""
    db = connect_db()
    cur = db.execute(query, args)
    db.commit()
    return cur.lastrowid


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    db = connect_db()
    rv = db.execute('select user_id from users where username = ?',
                    [username]).fetchone()
    return rv[0] if rv else None


def execute_db(query, args=()):
    db = connect_db()
    db.execute(query, args)
    db.commit()
