from fastapi import APIRouter, HTTPException, Request, Response, Form, Query
from fastapi.responses import RedirectResponse
from database import execute_db, get_user_id, query_db
from typing import Union
import time

router = APIRouter()


@router.get("/api/users/{username}/followers")
def _(request: Request, username: str, no: Union[str, None] = Query(default=100)):
    user_id = request.session['user_id']
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authorized")

    query = """SELECT user.username FROM user
                WHERE follower.who_id=%s
                LIMIT %s"""
    followers = query_db(query, [user_id, no])
    follower_names = [f["username"] for f in followers]
    return {"follows": follower_names}


@router.get("/api/users/{username}/follow")
def follow_user(request: Request, username: str):
    """Adds the current user as follower of the given user."""
    user_id = request.session['user_id']

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    whom_id = get_user_id(username)
    if whom_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    execute_db('insert into followers (who_id, whom_id) values (%s, %s)',
               [user_id, whom_id])

    # todo add flash message
    return RedirectResponse("/timeline/"  + username, status_code=302)


@router.get("/api/users/{username}/unfollow")
def unfollow_user(request: Request, username: str):
    user_id = request.session['user_id']

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    whom_id = get_user_id(username)
    if whom_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    execute_db('delete from followers where who_id=%s and whom_id=%s',
               [user_id, whom_id])

    # todo add flash message
    return RedirectResponse("/timeline/" + username, status_code=302)


@router.post("/api/users/messages")
def post_message(request: Request, response: Response, text: str = Form(..., min_length=1)):
    """Registers a new message for the user."""
    user_id = request.session['user_id']

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authorized")

    execute_db('''insert into messages (author_id, text, pub_date, flagged)
            values (%s, %s, %s, 0)''', [user_id, text, int(time.time())])
    return RedirectResponse("/", status_code=302)
