"""
Admin panel — FAQAT config.py dagi ADMIN_ID ga mos foydalanuvchi uchun ishlaydi.
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMIN_ID
import database
import texts

router = Router()


def _is_admin(message: Message) -> bool:
    return message.from_user.id == ADMIN_ID


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not _is_admin(message):
        await message.answer(texts.NOT_ADMIN)
        return
    await message.answer(texts.ADMIN_MENU)


@router.message(Command("stats"))
async def admin_stats(message: Message):
    if not _is_admin(message):
        await message.answer(texts.NOT_ADMIN)
        return
    totals = await database.get_total_counts()
    activity = await database.get_activity_since(30)
    await message.answer(
        "📊 <b>Umumiy statistika</b>\n\n"
        f"👥 Jami foydalanuvchilar: {totals['total_users']}\n"
        f"📚 Jami bajarilgan mashqlar: {totals['total_exercises']}\n\n"
        f"So'nggi 30 daqiqada:\n"
        f"🆕 Yangi foydalanuvchilar: {activity['new_users']}\n"
        f"🎯 Mashqlar: {activity['new_exercises']}\n"
        f"📊 O'rtacha natija: {activity['avg_score']}%"
    )
