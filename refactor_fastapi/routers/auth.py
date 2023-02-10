from fastapi import APIRouter, Form
from database import query_db, insert_in_db

router = APIRouter()


@router.post("/api/auth/login")
def login(username: str = Form(), password: str = Form()):
    # TODO get user_id from the session
    user = query_db('''
        select * from user where username = ?''',
                    [username], one=True)
    if user is None or not hash(password) == user['pw_hash']:
        return {"error": "username not found"}
    else:
        # TODO show the timeline if auth is correct
        return {"success": "login success"}

# TODO validation


@router.post("/api/auth/register")
def register(username: str = Form(), email: str = Form(), password: str = Form()):
    user = query_db('''
        select * from user where username = ?''',
                    [username], one=True)
    if user is not None:
        return {"error": "username already exists"}
    else:
        insert_in_db('''
            insert into user (username, email, pw_hash)
            values (?, ?, ?)''',
                     [username, email, hash(password)])
        return {"success": "register success"}


@router.get("/api/auth/logout")
def logout():
    # todo delete session
    pass
