from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
import routers
import util
from dotenv import dotenv_values

dotenv = dotenv_values('.env')


# configuration
SECRET_KEY = dotenv['SESSION_SECRET_KEY']
PER_PAGE = 30
DEBUG = True

app = FastAPI()

# middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# import routers
app.include_router(routers.simulation_mapper_router)
app.include_router(routers.pages_router)
app.include_router(routers.timelines_router)
app.include_router(routers.users_router)
app.include_router(routers.auth_router)

app.mount("/static", StaticFiles(directory="static"), name="static")