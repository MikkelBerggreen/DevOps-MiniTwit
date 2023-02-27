import time
from typing import Union
from pydantic import BaseModel
from fastapi import APIRouter, Request, Response, Form, Query
from fastapi.responses import RedirectResponse

from services.implementions.auth_service import Auth_Service
from services.implementions.user_service import User_Service

router = APIRouter()

auth_service = Auth_Service()
user_service = User_Service()

@router.get("/msgs")
def _():
    return RedirectResponse("/api/timelines/public", status_code=307)

# This is a route that bypasses authorization and our session so it is implemented here
@router.get("/msgs/{username}", status_code=204)
def _(username: str, latest: Union[str, None] = Query(default=100)):
    return RedirectResponse(f"/api/timelines/{username}?PER_PAGE={latest}", status_code=307)

class MessageBody(BaseModel):
    content: Union[str, None]
# This is a route that bypasses authorization and our session so it is implemented here
@router.post("/msgs/{username}", status_code=200)
def _(request: Request, username: str, body: MessageBody):
    
    user_id = user_service.get_user_id_from_username(username)
    if user_id is None:
        return Response(status_code=403)
    
    user_service.post_message(user_id, body.content)
    # passing a body when redirecting is not supported
    # https://github.com/tiangolo/fastapi/issues/3963
    # thus, I must implement the route here

    return 'Your message "%s" was recorded' % body.content

class Registration(BaseModel):
    username: str
    email: str
    pwd: str

@router.post("/register", status_code=204)
def _(response: Response, body: Registration):
    if auth_service.check_if_user_exists(body.username):
        response.status_code = 403
        return {"error": "username already exists"}
    else:
        response.status_code = 204
        auth_service.register_user(body.username, body.email, body.pwd)
        return {"success": "register success"}


class FollowMessage(BaseModel):
    follow: Union[str, None]
    unfollow: Union[str, None]

@router.get("/fllws/{username}")
def _(username: str, response: Response, no: Union[str, None] = Query(default=100)):
    user_id = user_service.get_user_id_from_username(username)
    if not user_id:
        response.status_code = 404
        return {"error": "user doesn't exist"}

    followers = user_service.get_all_followers(user_id, no)
    response.status_code = 200
    follower_names = [f["username"] for f in followers]
    return {"follows": follower_names}

@router.post("/fllws/{username}")
def _(username: str, response: Response, body: FollowMessage):
    user_id = user_service.get_user_id_from_username(username)
    if user_id is None:
        return Response(status_code=403)

    if body.follow is not None:
    
        if not user_service.add_follower(user_id, body.follow):
            response.status_code = 404
            return {"error": "user doesn't exist"}
        response.status_code = 204
        return ""

    elif body.unfollow is not None:
        if not user_service.remove_follower(user_id, body.unfollow):
            response.status_code = 404
            return {"error": "user doesn't exist"}

        response.status_code = 204
        return ""

    return {"error": "invalid request: missing the value of 'follow' or 'unfollow' in the body"}

    