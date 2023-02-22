from services.implementions.auth_service import Auth_Service
from fastapi import APIRouter, Form, Request, Response
from database import query_db, insert_in_db
from fastapi.responses import RedirectResponse
import hashlib

router = APIRouter()

auth_service = Auth_Service()

@router.post("/api/auth/login")
def login(request: Request, username: str = Form(""), password: str = Form("")):
    user = auth_service.validate_user(username, password)
    if user is None:
        request.session['error'] = "username not found"
        return RedirectResponse("/login", status_code=302)
    else:
        request.session.pop('error', None)
        request.session['user_id'] = user['user_id']
        return RedirectResponse("/", status_code=302)


@router.post("/api/auth/register")
def register(request: Request, response: Response, username: str = Form(""), email: str = Form(""), password: str = Form("")):
    if auth_service.check_if_user_exists(username):
        response.status_code = 403
        request.session['error'] = "username already exists"
        return RedirectResponse("/register", status_code=302)
    else:
        request.session.pop('error', None)
        response.status_code = 204
        auth_service.register_user(username,email,password)
        return RedirectResponse("/login", status_code=302)


@router.get("/logout")
def logout(request: Request):
    request.session.pop('user_id', None)
    return RedirectResponse("/public", status_code=302)
