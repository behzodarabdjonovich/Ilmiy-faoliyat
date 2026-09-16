from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.bot.filters.admin import IsAdmin
from app.database.models import User, Letter
router=Router(); router.message.filter(IsAdmin())
@router.message(F.text=="👨‍💼 Admin panel")
async def admin(m:Message,session:AsyncSession):
    users=(await session.execute(select(func.count(User.id)))).scalar_one(); letters=(await session.execute(select(func.count(Letter.id)))).scalar_one()
    await m.answer(f"👨‍💼 Admin panel\n\n👥 Foydalanuvchilar: {users}\n📄 Xatlar: {letters}")
