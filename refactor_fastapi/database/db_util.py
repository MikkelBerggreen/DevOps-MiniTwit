import sqlite3
from contextlib import closing

# todo - refactor to avoid duplicate
DATABASE_URL = './minitwit.db'

def connect_db(DATABASE_URL):
    """Returns a new connection to the database."""
    return sqlite3.connect(DATABASE_URL)

def init_db():
    """Creates the database tables."""
    pass
"""     with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit() """
    
def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    db = connect_db(DATABASE_URL)
    cur = db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def insert_in_db(query, args=()):
    """Queries the database and returns a list of dictionaries."""
    db = connect_db(DATABASE_URL)
    cur = db.execute(query, args)
    db.commit()
    return cur.lastrowid

def get_user_id(username):
    """Convenience method to look up the id for a username."""
    db = connect_db(DATABASE_URL)
    rv = db.execute('select user_id from user where username = ?',
                       [username]).fetchone()
    return rv[0] if rv else None

def execute_db(query, args=()):
    db = connect_db(DATABASE_URL)
    db.execute(query, args)
    db.commit()