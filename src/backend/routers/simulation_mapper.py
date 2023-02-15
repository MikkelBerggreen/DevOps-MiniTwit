import time
from typing import Union
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
    print("*"*100)
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
    execute_db('''insert into message (author_id, text, pub_date, flagged)
            values (?, ?, ?, 0)''', [user_id, content, int(time.time())])
    return 'Your message "%s" was recorded' % content

@router.post("/register")
def _():
    return RedirectResponse("/api/auth/register", status_code=307)


# @router.post("/fllws/{username}")
# def _(username: str):
