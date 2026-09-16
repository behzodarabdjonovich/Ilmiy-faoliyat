from aiogram.filters import BaseFilter
from aiogram.types import Message
from app.config import get_settings
class IsAdmin(BaseFilter):
    async def __call__(self,message:Message)->bool: return bool(message.from_user and message.from_user.id in get_settings().admins)
