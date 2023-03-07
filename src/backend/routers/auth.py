from services.implementions.auth_service import Auth_Service
from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import RedirectResponse

from util.custom_exceptions import Custom_Exception
router = APIRouter()

auth_service = Auth_Service()


@router.post("/api/auth/login")
def login(
    request: Request,
    response: Response,
    username: str = Form(""),
    password: str = Form("")
):
    request.session.pop("error", None)
    try:
        user = auth_service.validate_user(username, password)
    except Custom_Exception as er:
        response.status_code = er.status_code
        request.session["error"] = er.msg
        return RedirectResponse("/login", status_code=302)
        
    response.status_code = 204
    request.session["user_id"] = user["user_id"]
    request.session["username"] = username
    return RedirectResponse("/", status_code=302)


@router.post("/api/auth/register")
def register(
    request: Request,
    response: Response,
    username: str = Form(""),
    email: str = Form(""),
    password: str = Form(""),
):
    request.session.pop("error", None)
    try:
        auth_service.register_user(username, email, password)
    except Custom_Exception as er:
        response.status_code = er.status_code
        request.session["error"] = er.msg
        return RedirectResponse("/register", status_code=302)

    response.status_code = 204

    return RedirectResponse("/login", status_code=302)


@router.get("/logout")
def logout(request: Request):
    request.session.pop("user_id", None)
    request.session.pop("username", None)
    return RedirectResponse("/public", status_code=302)
