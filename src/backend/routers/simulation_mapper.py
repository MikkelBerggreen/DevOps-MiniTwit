import time
from typing import Union
from pydantic import BaseModel
from fastapi import APIRouter, Request, Response, Form, Query
from fastapi.responses import RedirectResponse
from database import query_db, insert_in_db, get_user_id, execute_db

router = APIRouter()

@router.get("/msgs")
def _():
    return RedirectResponse("/api/timelines/", status_code=307)

# This is a route that bypasses authorization and our session so it is implemented here
@router.get("/msgs/{username}", status_code=204)
def _(username: str, latest: Union[str, None] = Query(default=100)):
    return RedirectResponse(f"/api/timelines/{username}?PER_PAGE={latest}", status_code=307)

# This is a route that bypasses authorization and our session so it is implemented here
@router.post("/msgs/{username}", status_code=204)
def _(request: Request, username: str, content: str = Form(default="")):
    user_id = get_user_id(username)
    if user_id is None:
        print("*"*100)
        print(user_id, username, "|")
        return Response(status_code=403)

    # passing a body when redirecting is not supported
    # https://github.com/tiangolo/fastapi/issues/3963
    # thus, I must implement the route here
    execute_db('''insert into message (author_id, text, pub_date, flagged)
            values (?, ?, ?, 0)''', [user_id, content, int(time.time())])
    return 'Your message "%s" was recorded' % content

class Registration(BaseModel):
    username: str
    email: str
    pwd: str

@router.post("/register", status_code=203)
def _(response: Response, body: Registration):
    user = query_db('''
        select * from user where username = ?''',
                    [body.username], one=True)
    if user is not None:
        response.status_code = 403
        return {"error": "username already exists"}
    else:
        insert_in_db('''
            insert into user (username, email, pw_hash)
            values (?, ?, ?)''',
                     [body.username, body.email, hash(body.pwd)])
    return {"success": "register success"}


# @router.post("/fllws/{username}")
# def _(username: str):
