"""
Admin uchun hisobotlarni shakllantirish va yuborish.
Talab: yangi foydalanuvchi ro'yxatdan o'tganda va mashq yakunlangach DARROV,
shuningdek faollik bo'lganda har 30 daqiqada umumiy hisobot yuboriladi.
"""
from datetime import datetime

from aiogram import Bot

from config import ADMIN_ID
import database


async def send_new_user_report(bot: Bot, user_data: dict):
    text = (
        "🆕 <b>Yangi foydalanuvchi ro'yxatdan o'tdi</b>\n\n"
        f"👤 Ism: {user_data.get('full_name')}\n"
        f"🎂 Yosh: {user_data.get('age')}\n"
        f"📍 Hudud: {user_data.get('region')}, {user_data.get('district')}\n"
        f"🎯 Maqsad: {user_data.get('goal')}\n"
        f"🗣 Tanlangan til: {user_data.get('target_language')}\n"
        f"⏰ Kunlik mashg'uloti: {user_data.get('daily_routine')}\n"
        f"🔎 E'tibor sohasi: {user_data.get('focus_area')}\n"
        f"🆔 Telegram ID: {user_data.get('telegram_id')}"
    )
    await bot.send_message(ADMIN_ID, text)


async def send_exercise_completed_report(bot: Bot, user_data: dict, exercise_summary: dict):
    text = (
        "✅ <b>Foydalanuvchi mashqni yakunladi</b>\n\n"
        f"👤 {user_data.get('full_name')} (ID: {user_data.get('telegram_id')})\n"
        f"🗣 Til: {exercise_summary.get('language')}\n"
        f"📊 Natija: {exercise_summary.get('score')}%\n"
        f"🕒 Vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
    await bot.send_message(ADMIN_ID, text)


async def send_periodic_summary(bot: Bot, minutes: int = 30):
    activity = await database.get_activity_since(minutes)
    if activity["new_users"] == 0 and activity["new_exercises"] == 0:
        return  # faollik bo'lmasa hisobot yuborilmaydi (spam qilmaslik uchun)

    totals = await database.get_total_counts()
    text = (
        f"📈 <b>So'nggi {minutes} daqiqalik hisobot</b> ({datetime.now().strftime('%H:%M')})\n\n"
        f"🆕 Yangi foydalanuvchilar: {activity['new_users']}\n"
        f"🎯 Bajarilgan mashqlar: {activity['new_exercises']}\n"
        f"📊 O'rtacha natija: {activity['avg_score']}%\n\n"
        f"👥 Jami foydalanuvchilar: {totals['total_users']}\n"
        f"📚 Jami mashqlar: {totals['total_exercises']}"
    )
    await bot.send_message(ADMIN_ID, text)
    await database.mark_report_sent("periodic_30min")
