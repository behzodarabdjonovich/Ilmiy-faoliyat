from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import get_settings
from app.database.repositories.users import get_or_create_user
from app.bot.keyboards.common import main_menu
router=Router()
@router.message(CommandStart())
async def start(m:Message,session:AsyncSession):
    u=m.from_user; await get_or_create_user(session,u.id,u.username,u.full_name)
    await m.answer("Assalomu alaykum. Rasmiy xatlar yordamchisiga xush kelibsiz.",reply_markup=main_menu(u.id in get_settings().admins))
@router.message(F.text=="ℹ️ Yordam")
async def help_(m:Message): await m.answer("📝 Yangi xat yaratish bo‘limida savollarga javob bering. AI faqat siz bergan faktlar asosida rasmiy matn tayyorlaydi.")
