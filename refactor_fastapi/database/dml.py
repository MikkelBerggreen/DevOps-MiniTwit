def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    # cur = g.db.execute(query, args)
    # rv = [dict((cur.description[idx][0], value)
    #            for idx, value in enumerate(row)) for row in cur.fetchall()]
    # return (rv[0] if rv else None) if one else rv
    pass

def get_user_id(username):
    """Convenience method to look up the id for a username."""
    # rv = g.db.execute('select user_id from user where username = ?',
    #                    [username]).fetchone()
    # return rv[0] if rv else None
    pass

    