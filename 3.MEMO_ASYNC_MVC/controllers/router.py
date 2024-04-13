from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from dependencies import get_db, get_password_hash, verify_password
from models import User
from schemas import UserCreate, UserLogin

router = APIRouter()
templates = Jinja2Templates(directory='templates')

# 회원가입
@router.post("/signup/")
async def signup(signup_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 먼저 username이 이미 존재하는지 확인
    result = await db.execute(select(User).where(User.username == signup_data.username))
    existing_user = result.scalars().first() 
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 동일 사용자 이름이 가입되어 있습니다.")

    hashed_password = get_password_hash(signup_data.password)
    new_user = User(
        username = signup_data.username, 
        email = signup_data.email, 
        hashed_password = hashed_password)
    db.add(new_user)
    
    # 혹시 모를 오류에 대비
    try:
        await db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="회원가입이 실패했습니다. 기입한 내용을 확인해보세요.")
    
    await db.refresh(new_user)
    return {"message": "회원가입이 성공했습니다."}

# 로그인
@router.post("/login/")
async def login(request: Request, signin_data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == signin_data.username))
    user = result.scalars().first()
    if user and verify_password(signin_data.password, user.hashed_password):
        request.session['username'] = user.username
        return {"message": "로그인이 성공했습니다."}
    else:
        raise HTTPException(status_code=401, detail="로그인이 실패했습니다.")

# 로그아웃
@router.post("/logout/")
async def logout(request: Request):
    request.session.pop('username', None)
    return {"message": "로그아웃이 성공했습니다."}

@router.get("/about")
async def about():
    return {"message": "이것은 마이 메모 앱의 소개 페이지입니다."}