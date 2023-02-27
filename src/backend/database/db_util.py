from contextlib import closing
from dotenv import dotenv_values
import psycopg2
dotenv = dotenv_values('.env')


# configuration
SECRET_KEY = dotenv['SESSION_SECRET_KEY']


def connect_db():
    """Returns a new connection to the database."""
    connection = psycopg2.connect(
        host= dotenv['POSTGRES_SERVER'],
        database= dotenv['POSTGRES_DB'],
        user= dotenv['POSTGRES_USER'],
        password= dotenv['POSTGRES_PASSWORD'],
        port= dotenv['POSTGRES_PORT']
    )
    return connection


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    db = connect_db().cursor()
    db.execute(query, args)
    rv = [dict((db.description[idx][0], value)
               for idx, value in enumerate(row)) for row in db.fetchall()]
    return (rv[0] if rv else None) if one else rv


def insert_in_db(query, args=()):
    """Queries the database and returns a list of dictionaries."""
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, args)
    db.commit()
    return cur.lastrowid


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    db = connect_db().cursor()
    db.execute('select user_id from users where username = %s',
                    [username])
    rv = db.fetchall()
    print(rv)
    return rv[0][0] if rv else None


def execute_db(query, args=()):
    db = connect_db()
    db.cursor().execute(query, args)
    db.commit()
