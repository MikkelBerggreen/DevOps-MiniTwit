from fastapi import APIRouter

router = APIRouter()

@router.get("/api/auth/login")
def login():
    """ todo auth check, and redirect if not logged in """
    pass

@router.post("/api/auth/login")
def login():
    """ todo auth check 
        show the timeline if auth is correct
    """
    pass

@router.get("/api/auth/register")
def register():
    """ todo auth check, and redirect if not logged in """
    pass

@router.post("/api/auth/register")
def register():
    pass


@router.get("/api/auth/logout")
def logout():
    pass