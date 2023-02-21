from fastapi import APIRouter, Form, Request, Response
from database import query_db, insert_in_db
from fastapi.responses import RedirectResponse
import hashlib

router = APIRouter()

@router.post("/api/auth/login")
def login(request: Request, username: str = Form(""), password: str = Form("")):
    user = query_db('''
        select * from users where username = ?''',
                    [username], one=True)
    
    hashed_pw = hashlib.md5(password.encode())
    if user is None or not hashed_pw.hexdigest() == user['pw_hash']:
        request.session['error'] = "username not found"
        return RedirectResponse("/login", status_code=302)
    else:
        request.session.pop('error', None)
        request.session['user_id'] = user['user_id']
        return RedirectResponse("/", status_code=302)

# TODO validation


@router.post("/api/auth/register")
def register(request: Request, username: str = Form(""), email: str = Form(""), password: str = Form("")):
    user = query_db('''
        select * from users where username = ?''',
                    [username], one=True)
    if user is not None:
        request.status_code = 403
        request.session['error'] = "username already exists"
        return RedirectResponse("/register", status_code=302)
    else:
        request.session.pop('error', None)
        request.status_code = 204
        hashed_pw = hashlib.md5(password.encode())
        insert_in_db('''
            insert into users (username, email, pw_hash)
            values (?, ?, ?)''',
                     [username, email, hashed_pw.hexdigest()])
        return RedirectResponse("/login", status_code=302)


@router.get("/logout")
def logout(request: Request):
    request.session.pop('user_id', None)
    return RedirectResponse("/public", status_code=302)
