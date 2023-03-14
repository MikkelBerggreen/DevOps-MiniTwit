from fastapi import APIRouter, HTTPException, Request, Response, Form, Query
from fastapi.responses import RedirectResponse
from typing import Union
from routers.pages import flash
from services.implementions.user_service import User_Service

router = APIRouter()
user_service = User_Service()


def get_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    return user_id


@router.get("/api/users/{username}/followers")
def _(request: Request,
        username: str,
        no: Union[str, None] = Query(default=100)):

    followers = user_service.get_all_followers(get_user(request), no)

    follower_names = [f["username"] for f in followers]
    return {"follows": follower_names}


@router.get("/api/users/{username}/follow")
def follow_user(request: Request, username: str):
    """Adds the current user as follower of the given user."""

    user_service.add_follower(get_user(request), username)
    flash(request, 'You are now following "%s"' % username, "Success")
    return RedirectResponse("/timeline/" + username, status_code=302)


@router.get("/api/users/{username}/unfollow")
def unfollow_user(request: Request, username: str):

    user_service.remove_follower(get_user(request), username)
    flash(request, 'You are no longer following "%s"' % username, "Success")
    return RedirectResponse("/timeline/" + username, status_code=302)


@router.post("/api/users/messages")
def post_message(request: Request, text: str = Form(..., min_length=1)):
    """Registers a new message for the user."""

    user_service.post_message(get_user(request), text)
    flash(request, 'Your message was recorded', "Success")
    return RedirectResponse("/", status_code=302)
