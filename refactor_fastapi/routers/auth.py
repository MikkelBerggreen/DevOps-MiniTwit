from fastapi import APIRouter

router = APIRouter()

# todo validation
@router.post("/api/auth/login")
def login():
    """ todo auth check 
        show the timeline if auth is correct
    """
    pass

# todo validation
@router.post("/api/auth/register")
def register():
    pass

@router.get("/api/auth/logout")
def logout():
    # todo delete session
    pass

