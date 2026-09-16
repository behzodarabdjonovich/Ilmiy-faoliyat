import asyncio, logging
from aiogram import Bot, Dispatcher
from app.config import get_settings
from app.bot.handlers import routers
from app.bot.middlewares.db import DbMiddleware
async def main():
    st=get_settings(); logging.basicConfig(level=getattr(logging,st.log_level.upper(),logging.INFO))
    bot=Bot(st.bot_token); dp=Dispatcher(); dp.update.middleware(DbMiddleware())
    for r in routers: dp.include_router(r)
    await bot.delete_webhook(drop_pending_updates=True); await dp.start_polling(bot)
if __name__=="__main__": asyncio.run(main())
