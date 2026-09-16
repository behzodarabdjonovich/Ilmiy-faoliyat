from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User
async def get_or_create_user(s:AsyncSession, telegram_id:int, username:str|None, full_name:str)->User:
    user=(await s.execute(select(User).where(User.telegram_id==telegram_id))).scalar_one_or_none()
    if user: return user
    user=User(telegram_id=telegram_id, username=username, full_name=full_name)
    s.add(user); await s.commit(); await s.refresh(user); return user
