from fastapi import APIRouter, HTTPException, Request, Response, Form, Query
from fastapi.responses import RedirectResponse
from typing import Union

from services.implementions.user_service import User_Service

router = APIRouter()


user_service = User_Service()

@router.get("/api/users/{username}/followers")
def _(request: Request, username: str, no: Union[str, None] = Query(default=100)):
    user_id = request.session.get('user_id')
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authorized")

    followers = user_service.get_all_followers(user_id, no)

    follower_names = [f["username"] for f in followers]
    return {"follows": follower_names}


@router.get("/api/users/{username}/follow")
def follow_user(request: Request, username: str):
    """Adds the current user as follower of the given user."""
    user_id = request.session.get('user_id')

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    
    if not user_service.add_follower(user_id, username):
        raise HTTPException(status_code=404, detail="User not found")

    # todo add flash message
    return RedirectResponse("/timeline/"  + username, status_code=302)


@router.get("/api/users/{username}/unfollow")
def unfollow_user(request: Request, username: str):
    user_id = request.session.get('user_id')

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    
    if not user_service.remove_follower(user_id, username):
        raise HTTPException(status_code=404, detail="User not found")
    
    # todo add flash message
    return RedirectResponse("/timeline/" + username, status_code=302)


@router.post("/api/users/messages")
def post_message(request: Request, response: Response, text: str = Form(..., min_length=1)):
    """Registers a new message for the user."""
    user_id = request.session.get('user_id')

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    
    user_service.post_message(user_id, text)

    return RedirectResponse("/", status_code=302)
