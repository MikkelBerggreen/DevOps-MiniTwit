from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
import routers
import util

# configuration
SECRET_KEY = '!secret'
PER_PAGE = 30
DEBUG = True

app = FastAPI()

# middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# import routers
app.include_router(routers.pages_router)
app.include_router(routers.timelines_router)
app.include_router(routers.users_router)
app.include_router(routers.auth_router)

