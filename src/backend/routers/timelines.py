from typing import Union
from fastapi import APIRouter, Query, HTTPException
from database import query_db

router = APIRouter()

@router.get("/api/timelines/", status_code=204)
def home_timeline(PER_PAGE: Union[int, None] = Query(default=30)):
    # todo auth check

    # todo get user_id from the session
    user_id = 1

    messages = query_db('''
        select message.*, user.* from message, user
        where message.flagged = 0 and message.author_id = user.user_id and (
            user.user_id = ? or
            user.user_id in (select whom_id from follower
                                    where who_id = ?))
        order by message.pub_date desc limit ?''',
        [user_id, user_id, PER_PAGE])
    return messages

@router.get("/api/timelines/public")
def public_timeline(PER_PAGE: Union[int, None] = Query(default=30)):
    messages = query_db('''
        select message.*, user.* from message, user
        where message.flagged = 0 and message.author_id = user.user_id
        order by message.pub_date desc limit ?;''', [PER_PAGE])
    return messages

@router.get("/api/timelines/{username}", status_code=204)
def user_timeline(username: str, PER_PAGE: Union[int, None] = Query(default=30)):
    profile_user = query_db('select * from user where username = ?',
                            [username], one=True)
    if profile_user is None:
        raise HTTPException(status_code=403, detail="User not found")
    else:
        messages = query_db('''
            select message.*, user.* from message, user
            where message.author_id = user.user_id and user.user_id = ?
            order by message.pub_date desc limit ?;''', [profile_user['user_id'], PER_PAGE])
        return messages


