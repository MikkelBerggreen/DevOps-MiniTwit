from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
import routers
from dotenv import dotenv_values

# style reference
import os

dotenv = dotenv_values(".env")

# configuration
if "SESSION_SECRET_KEY" in dotenv:
    SECRET_KEY = dotenv["SESSION_SECRET_KEY"]
else:
    SECRET_KEY = "Test"
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


script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "styles/")
app.mount("/static", StaticFiles(directory=st_abs_file_path), name="styles")
