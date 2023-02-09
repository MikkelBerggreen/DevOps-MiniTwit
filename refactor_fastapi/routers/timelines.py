from fastapi import APIRouter

router = APIRouter()

@router.get("/api/timelines/public")
def public_timeline():
    pass

@router.get("/api/timelines/{username}")
def public_timeline(username: str):
    pass


