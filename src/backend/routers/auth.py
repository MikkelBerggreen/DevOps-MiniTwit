from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import RedirectResponse
from routers.pages import flash
from services.implementions.auth_service import Auth_Service
import re
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

    error = ""

    if username == "":
        error = "Usename cannot be blank"
    elif password == "":
        error = "Usename cannot be blank"

    if error != "":
        response.status_code = 403
        request.session["error"] = error
        return RedirectResponse("/login", status_code=302)

    try:
        user = auth_service.validate_user(username, password)
        response.status_code = 204
        request.session["user_id"] = user.user_id
        request.session["username"] = username
        flash(request, 'You were logged in', "Success")
        return RedirectResponse("/", status_code=302)
    except Custom_Exception as er:
        response.status_code = er.status_code
        request.session["error"] = er.msg
        return RedirectResponse("/login", status_code=302)


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


@router.post("/api/auth/register")
def register(
    request: Request,
    response: Response,
    username: str = Form(""),
    email: str = Form(""),
    password: str = Form(""),
    password2: str = Form(""),
):
    request.session.pop("error", None)

    error = ""

    if username == "":
        error = "Username cannot be blank"
    elif email == "" or not re.fullmatch(regex, email):
        error = "You have to enter a valid email address"
    elif password == "":
        error = "Password cannot be blank"
    elif password != password2:
        error = "The two passwords do not match"
        
    if error != "":
        response.status_code = 403
        request.session["error"] = error
        return RedirectResponse("/register", status_code=302)

    try:
        auth_service.register_user(username, email, password)

        response.status_code = 204
        flash(request, "You are registered. You can now log in!", "Success")

        return RedirectResponse("/login", status_code=302)
    except Custom_Exception as er:
        response.status_code = er.status_code
        request.session["error"] = er.msg
        return RedirectResponse("/register", status_code=302)


@router.get("/logout")
def logout(request: Request):
    request.session.pop("user_id", None)
    request.session.pop("username", None)
    flash(request, "You were logged out", "Success")
    return RedirectResponse("/public", status_code=302)
