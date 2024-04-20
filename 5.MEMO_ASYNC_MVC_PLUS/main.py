from fastapi import FastAPI, Request, Depends
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from model.databases.mysql import engine, Base
from controller.users import users
from controller.memos import memos
from contextlib import asynccontextmanager
from settings import Settings
from module import app_settings

'''
*** 4.MEMO_ASYNC_MVC에서 수정할 부분 ***
1. 메모 CRUD를 mongodb로 교체
'''


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        lifespan=app_lifespan,
    )
 
    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
    app.include_router(users)
    app.include_router(memos, prefix="/memos")
    return app

templates = Jinja2Templates(directory="templates")

application: FastAPI = create_app(Settings())

@application.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@application.get("/test")
async def read_root(
    settings: Settings = Depends(app_settings)
):
    return {"test": settings.test_env}