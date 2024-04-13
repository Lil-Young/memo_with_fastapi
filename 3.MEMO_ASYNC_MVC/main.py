from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from database import engine, Base
from controllers.router import router
from controllers.memos import memos
from contextlib import asynccontextmanager

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# Swagger UI와 Redoc 도 비활성화합니다.
app = FastAPI(lifespan=app_lifespan, docs_url=None, redoc_url=None)
app.add_middleware(SessionMiddleware, secret_key = "ddddd")
app.include_router(router)
app.include_router(memos)
templates = Jinja2Templates(directory='templates')

@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})