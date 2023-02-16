from fastapi import APIRouter, HTTPException, Request, Response, Form
from database import execute_db, get_user_id
import time

router = APIRouter()


@router.get("/api/users/{username}/follow")
def follow_user(request: Request, username: str):
    """Adds the current user as follower of the given user."""
    user_id = request.session['user_id']

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    whom_id = get_user_id(username)
    if whom_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    execute_db('insert into follower (who_id, whom_id) values (?, ?)',
                [user_id, whom_id])
    
    # todo add flash message
    return 'You are now following "%s"' % username

    
@router.get("/api/users/{username}/unfollow")
def unfollow_user(request: Request, username: str):
    user_id = request.session['user_id']

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    whom_id = get_user_id(username)
    if whom_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    execute_db('delete from follower where who_id=? and whom_id=?',
                [user_id, whom_id])
    
    # todo add flash message
    return 'You are no longer following "%s"' % username

@router.post("/api/users/messages")
def post_message(request: Request, response: Response, content: str = Form(..., min_length=1)):
    """Registers a new message for the user."""
    user_id = request.session['user_id']

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authorized")

    execute_db('''insert into message (author_id, text, pub_date, flagged)
            values (?, ?, ?, 0)''', [user_id, content, int(time.time())])
    response.status_code = 204
    return 'Your message "%s" was recorded' % content
