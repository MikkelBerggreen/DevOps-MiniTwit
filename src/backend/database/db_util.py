import sqlite3
from contextlib import closing
import psycopg2
from os import environ

def connect_db():
    """Returns a new connection to the database."""
    connection = psycopg2.connect(
        host=environ.get("DB_HOST"),
        database=environ.get("DB_NAME"),
        user=environ.get("DB_USER"),
        password=environ.get("DB_PASSWORD"),
        port=environ.get("DB_PORT")
    )
    return connection.cursor()


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    db = connect_db()
    db.execute(query, args)
    rv = [dict((db.description[idx][0], value)
               for idx, value in enumerate(row)) for row in db.fetchall()]
    return (rv[0] if rv else None) if one else rv


def insert_in_db(query, args=()):
    """Queries the database and returns a list of dictionaries."""
    db = connect_db()
    db.execute(query, args)
    return db.lastrowid


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    db = connect_db()
    rv = db.execute('select user_id from users where username = %s',
                    [username]).fetchone()
    return rv[0] if rv else None


def execute_db(query, args=()):
    db = connect_db()
    db.execute(query, args)
