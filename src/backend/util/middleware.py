from fastapi import FastAPI, Request

middleware_app = FastAPI()

@middleware_app.middleware("http")
async def authorize_user(request: Request, call_next):
    if request.url.path.startswith("/api/auth"):
        if request.session["user_id"] is None:
           return {"error": "not logged in"}
    return await call_next(request)

