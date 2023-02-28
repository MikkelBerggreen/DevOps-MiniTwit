from typing import Union
from fastapi import APIRouter, Query, HTTPException

from services.implementions.timeline_service import Timeline_Service
from services.implementions.auth_service import Auth_Service

router = APIRouter()
timeline_service = Timeline_Service()
auth_service = Auth_Service()


@router.get("/api/timelines/", status_code=200)
def home_timeline(PER_PAGE: Union[int, None] = Query(default=30)):
    # todo auth check

    # todo get user_id from the session
    user = "Test"

    messages = timeline_service.get_user_timeline(user, PER_PAGE)
    return messages

@router.get("/api/timelines/public")
def public_timeline(PER_PAGE: Union[int, None] = Query(default=30)):
    messages = timeline_service.get_public_timeline(PER_PAGE)
    # Messy way of doing conversion. Change it later !
    for x in messages:
        x['content'] = x['text']
        x['user'] = x['username']
    return messages

@router.get("/api/timelines/{username}", status_code=204)
def user_timeline(username: str, PER_PAGE: Union[int, None] = Query(default=30)):
    if not auth_service.check_if_user_exists(username):
        raise HTTPException(status_code=404, detail="User not found")
    else:
        messages = timeline_service.get_follower_timeline(username ,PER_PAGE)
        for x in messages:
            x['content'] = x['text']
            x['user'] = x['username']
        return messages
