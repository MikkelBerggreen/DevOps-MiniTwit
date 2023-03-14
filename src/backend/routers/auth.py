from services.implementions.auth_service import Auth_Service
from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import RedirectResponse
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
    request.session.pop("success", None)
    if username == "":
        response.status_code = 403
        request.session["error"] =  "Usename cannot be blank"
        return RedirectResponse("/login", status_code=302)

    if password == "":
        response.status_code = 403
        request.session["error"] =  "Password cannot be blank"
        return RedirectResponse("/login", status_code=302)

    try:
        user = auth_service.validate_user(username, password)
    except Custom_Exception as er:
        response.status_code = er.status_code
        request.session["error"] = er.msg
        return RedirectResponse("/login", status_code=302)

    response.status_code = 204
    request.session["user_id"] = user.user_id
    request.session["username"] = username
    return RedirectResponse("/", status_code=302)

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
 
# Define a function for
# for validating an Email
def check(email):
 
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        print("Valid Email")
 
    else:
        print("Invalid Email")

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
    request.session.pop("success", None)
    if username == "":
        response.status_code = 403
        request.session["error"] = "Username cannot be blank"
        return RedirectResponse("/register", status_code=302)

    if email == "":
        response.status_code = 403
        request.session["error"] =  "Email cannot be blank"
        return RedirectResponse("/register", status_code=302)

    if not re.fullmatch(regex, email):
        response.status_code = 403
        request.session["error"] =  "You have to enter a valid email address"
        return RedirectResponse("/register", status_code=302)

    if password == "":
        response.status_code = 403
        request.session["error"] =  "Password cannot be blank"
        return RedirectResponse("/register", status_code=302)

    if password != password2:
        response.status_code = 403
        request.session["error"] =  "The two passwords do not match"
        return RedirectResponse("/register", status_code=302)

    try:
        auth_service.register_user(username, email, password)
    except Custom_Exception as er:
        response.status_code = er.status_code
        request.session["error"] = er.msg
        return RedirectResponse("/register", status_code=302)

    response.status_code = 204
    request.session["success"] = "You are registered. You can now log in!"
    return RedirectResponse("/login", status_code=302)


@router.get("/logout")
def logout(request: Request):
    request.session.pop("user_id", None)
    request.session.pop("username", None)
    return RedirectResponse("/public", status_code=302)
