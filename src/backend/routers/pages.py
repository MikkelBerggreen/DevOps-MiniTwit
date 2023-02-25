from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Union
import typing

from services.implementions.timeline_service import Timeline_Service
from services.implementions.auth_service import Auth_Service
from services.implementions.user_service import User_Service
import os

router = APIRouter()
script_dir = os.path.dirname(os.path.dirname((__file__)))

st_abs_file_path = os.path.join(script_dir, "templates")
templates = Jinja2Templates(directory=st_abs_file_path)

timeline_service = Timeline_Service()
user_service = User_Service()
auth_service = Auth_Service()

def flash(request: Request, message: typing.Any, category: str = "") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append({"message": message, "category": category})


def get_flashed_messages(request: Request):
    print(request.session)
    return request.session.pop("_messages") if "_messages" in request.session else []

templates.env.globals['get_flashed_messages'] = get_flashed_messages

def get_session(request, key):
    if key in request.session:
        return request.session[key]
    return None

@router.get("/", response_class=HTMLResponse)
def timeline(request: Request, PER_PAGE: Union[int, None] = Query(default=30)):
    user = get_session(request, 'user_id')
    username = get_session(request, 'username')
    endpoint = str(request.__getitem__('endpoint')).split(" ")[1]
    return templates.TemplateResponse("timeline.html", {"request": request, "g": username, "endpoint": endpoint, "messages": timeline_service.get_user_timeline(user, PER_PAGE)})

@router.get("/public", response_class=HTMLResponse)
def public_timeline(request: Request, PER_PAGE: Union[int, None] = Query(default=30)):
    username = get_session(request, 'username')
    endpoint = str(request.__getitem__('endpoint')).split(" ")[1]

    return templates.TemplateResponse("timeline.html", {"request": request, "g": username, "endpoint": endpoint, "messages": timeline_service.get_public_timeline(PER_PAGE)})

@router.get("/timeline/{username}", response_class=HTMLResponse)
def user_timeline(request: Request, username: str, PER_PAGE: Union[int, None] = Query(default=30)):

    if not auth_service.check_if_user_exists(username):
        raise HTTPException(status_code=404, detail="User not found")
    followed = False
    endpoint = str(request.__getitem__('endpoint')).split(" ")[1]
    if get_session(request, 'user_id'):
        followed =user_service.check_if_following(get_session(request, 'user_id'), username)

    profile_user = {"user_id": user_service.get_user_id_from_username(username), "username": username}
    return templates.TemplateResponse('timeline.html', {"request": request, "messages": timeline_service.get_follower_timeline(username ,PER_PAGE), "followed": followed, "profile_user": profile_user, "endpoint": endpoint, "g":  get_session(request, 'username'),  "f":  get_session(request, 'user_id')}) 

@router.get("/login", response_class=HTMLResponse)
def login(request: Request, PER_PAGE: Union[int, None] = Query(default=30)):
    """ todo auth check, and redirect if not logged in """
    user = get_session(request, 'user_id')
    username = get_session(request, 'username')
    if user:
        return RedirectResponse("/", status_code=307)
    
    return templates.TemplateResponse('login.html', {"request": request, "error": get_session(request, 'error'), "g":username})

@router.get("/register", response_class=HTMLResponse)
def register(request: Request):
    """ todo auth check, and redirect if not logged in """
    user = get_session(request, 'user_id')
    username = get_session(request, 'username')
    
    if user:
        return RedirectResponse("/", status_code=307)
    
    return templates.TemplateResponse('register.html', {"request": request, "error": get_session(request, 'error'), "g": username})

