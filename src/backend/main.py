from fastapi import FastAPI , Request

from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from util.custom_exceptions import Custom_Exception
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


@app.exception_handler(Custom_Exception)
async def unicorn_exception_handler(request: Request, exc: Custom_Exception):
    request.session["error"] = exc.msg
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": f"{exc.msg}"},
    )
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
