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
        return Response(status_code=403)

    # passing a body when redirecting is not supported
    # https://github.com/tiangolo/fastapi/issues/3963
    # thus, I must implement the route here
    execute_db('''insert into messages (author_id, text, pub_date, flagged)
            values (?, ?, ?, 0)''', [user_id, content, int(time.time())])
    return 'Your message "%s" was recorded' % content

class Registration(BaseModel):
    username: str
    email: str
    pwd: str

@router.post("/register", status_code=204)
def _(response: Response, body: Registration):
    user = query_db('''
        select * from users where username = ?''',
                    [body.username], one=True)
    if user is not None:
        response.status_code = 403
        return {"error": "username already exists"}
    else:
        insert_in_db('''
            insert into users (username, email, pw_hash)
            values (?, ?, ?)''',
                     [body.username, body.email, hash(body.pwd)])
    return {"success": "register success"}

class FollowMessage(BaseModel):
    follow: Union[str, None]
    unfollow: Union[str, None]

@router.get("/fllws/{username}")
def _(username: str, no: Union[str, None] = Query(default=100)):
    return RedirectResponse(f"/api/users/{username}/followers?no={no}", status_code=307)

@router.post("/fllws/{username}")
def _(username: str, response: Response, body: FollowMessage):
    user_id = get_user_id(username)
    if user_id is None:
        return Response(status_code=403)

    if body.follow is not None:
        follows_username = body.follow
        follows_user_id = get_user_id(follows_username)
        if not follows_user_id:
            response.status_code = 404
            return {"error": "user doesn't exist"}
        insert_in_db('''
            INSERT INTO followers (who_id, whom_id) VALUES (?, ?)''',
            [user_id, follows_user_id])
        response.status_code = 204
        return ""

    elif body.unfollow is not None:
        unfollows_username = body.unfollow
        unfollows_user_id = get_user_id(unfollows_username)
        if not unfollows_user_id:
            response.status_code = 404
            return {"error": "user doesn't exist"}
        insert_in_db('''
            DELETE FROM followers WHERE who_id=? and WHOM_ID=?''',
            [user_id, unfollows_user_id])
        response.status_code = 204
        return ""
