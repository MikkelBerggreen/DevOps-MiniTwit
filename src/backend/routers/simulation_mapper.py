import time
from typing import Union
from fastapi import APIRouter, Response, Form, Query
from fastapi.responses import RedirectResponse
from database import query_db, insert_in_db, get_user_id

router = APIRouter()

@router.get("/msgs")
def _():
    return RedirectResponse("/api/timelines/", status_code=307)

# This is a route that bypasses authorization and our session so it is implemented here
@router.get("/msgs/{username}")
def _(response: Response, username: str, no: Union[str, None] = Query(default=100)):
    user_id = get_user_id(username)
    if not user_id:
        response.status_code = 403
        return

    number_of_messages = no
    query = """SELECT message.*, user.* FROM message, user 
                WHERE message.flagged = 0 AND
                user.user_id = message.author_id AND user.user_id = ?
                ORDER BY message.pub_date DESC LIMIT ?"""
    messages = query_db(query, [user_id, number_of_messages])

    return messages

# This is a route that bypasses authorization and our session so it is implemented here
@router.post("/msgs/{username}", status_code=204)
def _(response: Response, username: str, content: str = Form("")):
    user_id = get_user_id(username)
    if not user_id:
        response.status_code = 403
        return
    insert_in_db("""INSERT INTO message (author_id, text, pub_date, flagged)
                   VALUES (?, ?, ?, 0)""",
                   [user_id, content, int(time.time())]
    )
    return 
    

@router.post("/register")
def _():
    return RedirectResponse("/api/auth/register", status_code=307)


# @router.post("/fllws/{username}")
# def _(username: str):
#     pass
#     # return RedirectResponse("/api/auth/register", status_code=307)