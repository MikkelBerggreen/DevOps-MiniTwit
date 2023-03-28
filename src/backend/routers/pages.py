from fastapi import APIRouter, Request, Query, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Union
import typing
from typing_extensions import Annotated
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

    request.session["_messages"].append({
        "message": message, "category": category
        })


def get_flashed_messages(request: Request):
    if "_messages" in request.session:
        return request.session.pop("_messages")

    return []


templates.env.globals["get_flashed_messages"] = get_flashed_messages


def common_parameters(
    no: int = 30,
    page: int = 1
):
    return {"no": no, "page": page}


def get_session(request, key):
    if key in request.session:
        return request.session[key]
    return None


def func(request: Request):
    request_args = dict(request.query_params)
    user = get_session(request, "user_id")
    if "no" not in request_args:
        request_args["no"] = 30

    if not user:
        raise HTTPException(
            status_code=307,
            headers={'Location': '/public?no='+str(request_args["no"])})
    return True

@router.get("/", response_class=HTMLResponse, dependencies=[Depends(func)])
def timeline(request: Request, commons: dict = Depends(common_parameters)):
    no, page = commons["no"], commons["page"]
    user = get_session(request, "user_id")
    username = get_session(request, "username")

    #if not user:
        #return RedirectResponse("/public?no=" + str(no), status_code=307)

    endpoint = str(request.__getitem__("endpoint")).split(" ")[1]
    template = templates.get_template("timeline.html")

    msg = timeline_service.get_user_timeline(user, no, page)

    next_url = "/?no=" + str(no) + "&page=" + str(page+1)\
        if len(msg) == no else None
    prev_url = "/?no=" + str(no) + "&page=" + str(page-1) \
        if page > 1 else None

    html = template.render({
        "request": request,
        "g": username,
        "endpoint": endpoint,
        "messages": msg,
        "next_url": next_url,
        "prev_url": prev_url, })
    return HTMLResponse(html)


@router.get("/public", response_class=HTMLResponse)
def public_timeline(
    request: Request, commons: dict = Depends(common_parameters)):
    no, page = commons["no"], commons["page"]

    username = get_session(request, "username")
    endpoint = str(request.__getitem__("endpoint")).split(" ")[1]
    template = templates.get_template("timeline.html")
    msg = timeline_service.get_public_timeline(no, page)
    next_url = "/public?no=" + str(no) + "&page=" + str(page+1)\
        if len(msg) == no else None
    prev_url = "/public?no=" + str(no) + "&page=" + str(page-1)\
        if page > 1 else None

    html = template.render({
        "request": request,
        "g": username,
        "endpoint": endpoint,
        "messages": msg,
        "next_url": next_url,
        "prev_url": prev_url,
        })
    return HTMLResponse(html)


@router.get("/timeline/{username}", response_class=HTMLResponse)
def user_timeline(username: str,
    request: Request, commons: dict = Depends(common_parameters)):
    no, page = commons["no"], commons["page"]
    auth_service.check_if_user_exists(username)

    followed = False
    endpoint = str(request.__getitem__("endpoint")).split(" ")[1]

    if get_session(request, "user_id"):
        followed = user_service.check_if_following(
            get_session(request, "user_id"), username
        )

    profile_user = {
        "user_id": user_service.get_user_id_from_username(username),
        "username": username,
    }
    msg = timeline_service.get_follower_timeline(username, no, page)
    next_url = "/timeline/"+username+"?no=" + str(no) + "&page=" + str(page+1)\
        if len(msg) == no else None
    prev_url = "/timeline/"+username+"?no=" + str(no) + "&page=" + str(page-1)\
        if page > 1 else None

    template = templates.get_template("timeline.html")
    html = template.render({
        "request": request,
        "messages": msg,
        "followed": followed,
        "profile_user": profile_user,
        "endpoint": endpoint,
        "g": get_session(request, "username"),
        "f": get_session(request, "user_id"),
        "next_url": next_url,
        "prev_url": prev_url, 
        })
    return HTMLResponse(html)


@router.get("/login", response_class=HTMLResponse)
def login(request: Request):
    """todo auth check, and redirect if not logged in"""
    user = get_session(request, "user_id")
    username = get_session(request, "username")

    if user:
        return RedirectResponse("/", status_code=307)

    template = templates.get_template("login.html")
    html = template.render({
        "request": request,
        "error": get_session(request, "error"),
        "g": username
        })
    return HTMLResponse(html)


@router.get("/register", response_class=HTMLResponse)
def register(request: Request):

    user = get_session(request, "user_id")
    username = get_session(request, "username")

    if user:
        return RedirectResponse("/", status_code=307)

    template = templates.get_template("register.html")
    html = template.render({
        "request": request,
        "error": get_session(request, "error"),
        "g": username
        })
    return HTMLResponse(html)
