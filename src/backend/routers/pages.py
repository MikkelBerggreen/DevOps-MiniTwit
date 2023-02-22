from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Union
import typing
from database import query_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


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
    endpoint = str(request.__getitem__('endpoint')).split(" ")[1]
    return templates.TemplateResponse("timeline.html", {"request": request, "g": user, "endpoint": endpoint, "messages": query_db('''
        select messages.*, users.* from messages, users
        where messages.flagged = 0 and messages.author_id = users.user_id and (
            users.user_id = %s or
            users.user_id in (select whom_id from followers
                                    where who_id = %s))
        order by messages.pub_date desc limit %s''',
        [user, user, PER_PAGE])})

@router.get("/public", response_class=HTMLResponse)
def public_timeline(request: Request, PER_PAGE: Union[int, None] = Query(default=30)):
    user = get_session(request, 'user_id')
    endpoint = str(request.__getitem__('endpoint')).split(" ")[1]
    print(query_db('''
        select messages.*, users.* from messages, users
        where messages.flagged = 0 and messages.author_id = users.user_id
        order by messages.pub_date desc limit %s''', [PER_PAGE]))
    return templates.TemplateResponse("timeline.html", {"request": request, "g": user, "endpoint": endpoint, "messages": query_db('''
        select messages.*, users.* from messages, users
        where messages.flagged = 0 and messages.author_id = users.user_id
        order by messages.pub_date desc limit %s''', [PER_PAGE])})

@router.get("/timeline/{username}", response_class=HTMLResponse)
def user_timeline(request: Request, username: str, PER_PAGE: Union[int, None] = Query(default=30)):
    profile_user = query_db('select * from users where username = %s',
                        [username], one=True)
    if profile_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    followed = False
    endpoint = str(request.__getitem__('endpoint')).split(" ")[1]
    if get_session(request, 'user_id'):
        followed = query_db('''select 1 from followers where
            followers.who_id = %s and followers.whom_id = %s''',
            [get_session(request, 'user_id'), profile_user['user_id']], one=True) is not None
    return templates.TemplateResponse('timeline.html', {"request": request, "messages": query_db('''
            select messages.*, users.* from messages, users where
            users.user_id = messages.author_id and users.user_id = %s
            order by messages.pub_date desc limit %s''',
            [profile_user['user_id'], PER_PAGE]), "followed": followed, "profile_user": profile_user, "endpoint": endpoint, "g":  get_session(request, 'user_id')}) 

@router.get("/login", response_class=HTMLResponse)
def login(request: Request, PER_PAGE: Union[int, None] = Query(default=30)):
    """ todo auth check, and redirect if not logged in """
    user = get_session(request, 'user_id')
    if user:
        return RedirectResponse("/", status_code=307)
    error = None
    return templates.TemplateResponse('login.html', {"request": request, "error": get_session(request, 'error'), "g":user})

@router.get("/register", response_class=HTMLResponse)
def register(request: Request):
    """ todo auth check, and redirect if not logged in """
    user = get_session(request, 'user_id')
    if user:
        return RedirectResponse("/", status_code=307)
    error = None
    return templates.TemplateResponse('register.html', {"request": request, "error": get_session(request, 'error'), "g": user})

