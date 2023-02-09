from fastapi import FastAPI
import database

# configuration
DATABASE_URL = './minitwit.db'
PER_PAGE = 30
DEBUG = True

app = FastAPI()

# database


# import routers
import routers

app.include_router(routers.pages_router)
app.include_router(routers.timelines_router)
app.include_router(routers.users_router)
app.include_router(routers.auth_router)



