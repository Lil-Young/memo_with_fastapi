from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .dependencies import get_db
from databases.models import User, Memo
from schemas import MemoCreate, MemoUpdate

memos = APIRouter()
templates = Jinja2Templates(directory="templates")

# 메모 생성
@memos.post("/")
async def create_memo(request: Request, memo: MemoCreate, db: AsyncSession = Depends(get_db)):
    username = request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401, detail="인증되지 않은 사용자입니다.")
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    new_memo = Memo(user_id=user.id, title=memo.title, content=memo.content)
    db.add(new_memo)
    await db.commit()
    await db.refresh(new_memo)
    return new_memo

# 메모 조회
@memos.get("/")
async def list_memos(request: Request, db: AsyncSession = Depends(get_db)):
    username = request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401, detail="인증되지 않은 사용자입니다.")
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    result = await db.execute(select(Memo).where(Memo.user_id == user.id))
    memos = result.scalars().all()
    return templates.TemplateResponse("memos.html", {"request": request, "memos": memos, "username": username})

# 메모 업데이트
@memos.put("/{memo_id}")
async def update_memo(request: Request, memo_id: int, memo: MemoUpdate, db: AsyncSession = Depends(get_db)):
    username = request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401, detail="인증되지 않은 사용자입니다.")
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    result = await db.execute(select(Memo).where(Memo.user_id == user.id, Memo.id == memo_id))
    db_memo = result.scalars().first()
    if db_memo is None:
        return {"error": "메모를 찾을 수 없습니다."}
    
    if memo.title is not None:
        db_memo.title = memo.title
    if memo.content is not None:
        db_memo.content = memo.content
    
    await db.commit()
    await db.refresh(db_memo)
    return db_memo

# 메모 삭제
@memos.delete("/{memo_id}")
async def delete_memo(request: Request, memo_id: int, db: AsyncSession = Depends(get_db)):
    username = request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401, detail="인증되지 않은 사용자입니다.")
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    result = await db.execute(select(Memo).where(Memo.id == memo_id, Memo.user_id == user.id))
    db_memo = result.scalars().first()
    if db_memo is None:
        return {"error": "메모를 찾을 수 없습니다."}
    
    await db.delete(db_memo)
    await db.commit()
    return {"message": "메모가 삭제되었습니다."}