# 의존성 함수들 
# get_password_hash 는 사용자가 회원가입할 때 입력한 비밀번호를 해시 할 때 사용(의존)함.
# verify_password 는 사용자가 로그인할 때 입력한 비밀번호와 DB에 저장된 비밀번호가 일치하는지 확인할 때 사용(의존)함.
# get_db 는 request(요청), response(응답)할 때 DB에 접근을 가능하게 해주기 위해 사용(의존)함.

from passlib.context import CryptContext
from database import AsyncSessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

async def get_password_hash(password):
    return pwd_context.hash(password)

async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_db():
    # with 안에서 파일을 오픈하면 파일 처리 후 자동으로 close(닫기)를 해준다.
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()