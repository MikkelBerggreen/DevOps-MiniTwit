from fastapi import FastAPI

# configuration
DATABASE = './minitwit.db'
PER_PAGE = 30
DEBUG = True

app = FastAPI()

# Import routers
import routers

app.include_router(routers.pages_router)
app.include_router(routers.timelines_router)
app.include_router(routers.users_router)
app.include_router(routers.auth_router)



# todo delete this.. i have it as an example
import database.connection as db

cursor = db.cursor()
cursor.execute('SELECT * FROM user LIMIT 4')


