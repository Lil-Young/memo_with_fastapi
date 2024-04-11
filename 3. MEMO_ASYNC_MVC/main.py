from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from database import engine, Base
from controllers import router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key = "ddddd")

# 데이터베이스의 테이블을 만드는 부분 정도는 맨 처음에 객체를 만들자마자 한 번 실행이 돼야하므로 controller에 넣어도 상관없을거 같다.
Base.metadata.create_all(bind=engine)

app.include_router(router)

templates = Jinja2Templates(directory='templates')

@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})