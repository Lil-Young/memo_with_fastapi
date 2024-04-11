# Pydantic의 BaseModel 관련 코드

from pydantic import BaseModel
from typing import Optional

# 회원가입시 데이터 검증
class UserCreate(BaseModel):
    username: str
    email: str
    password: str # 해시전 패스워드를 받습니다.

class UserLogin(BaseModel):
    username: str
    password: str # 해시전 패스워드를 받습니다.

class MemoCreate(BaseModel):
    title: str
    content: str

class MemoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
