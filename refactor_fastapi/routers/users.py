from fastapi import APIRouter

router = APIRouter()

@router.get("/api/users/{username}/follow")
def follow_user(username: str):
    # todo should redirect if we use Jinja
    pass

@router.get("/api/users/{username}/unfollow")
def follow_user(username: str):
    # todo should redirect if we use Jinja
    pass

@router.post("/api/users/messages")
def post_message():
    # todo should redirect if we use Jinja
    pass

