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

@router.get("/login")
def login():
    """ todo auth check, and redirect if not logged in """
    pass

@router.get("/register")
def register():
    """ todo auth check, and redirect if not logged in """
    pass

