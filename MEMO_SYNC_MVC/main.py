from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from database import engine, Base
from controllers import router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key = "ddddd")

Base.metadata.create_all(bind=engine)

app.include_router(router)

templates = Jinja2Templates(directory='templates')

@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})