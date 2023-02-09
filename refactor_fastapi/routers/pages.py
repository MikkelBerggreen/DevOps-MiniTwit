from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def timeline():
    return {"message": "This is the timeline"}

@router.get("/public")
def public_timeline():
    return {"message": "This is the public timeline"}

@router.get("/{username}")
def user_timeline(username: str):
    return {"message": "This is the user specific timeline"}


