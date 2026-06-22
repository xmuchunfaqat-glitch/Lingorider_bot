"""
Lingorider_bot — asosiy ishga tushirish fayli.
Ishlatish: python bot.py
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, ADMIN_ID
import database
import handlers_start
import handlers_exercises
import handlers_menu
import handlers_admin
from scheduler_service import setup_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lingorider")


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN topilmadi. .env faylini tekshiring (.env.example dan ko'chiring).")
    if not ADMIN_ID:
        raise RuntimeError("ADMIN_ID topilmadi. .env faylida ADMIN_ID ni o'rnating.")

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(handlers_admin.router)   # admin buyruqlari birinchi tekshirilsin
    dp.include_router(handlers_start.router)
    dp.include_router(handlers_exercises.router)
    dp.include_router(handlers_menu.router)

    await database.init_db()
    logger.info("Ma'lumotlar bazasi tayyor.")

    setup_scheduler(bot)
    logger.info("Hisobot rejalashtiruvchisi (har 30 daqiqa) ishga tushdi.")

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Lingorider_bot ishga tushdi. To'xtatish uchun Ctrl+C bosing.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
