"""
Har 30 daqiqada (Toshkent vaqti bo'yicha) adminga umumiy hisobot yuborish uchun
fon vazifasi (background job).
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import pytz

from aiogram import Bot

from config import TIMEZONE, REPORT_INTERVAL_MINUTES
import report_service


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    tz = pytz.timezone(TIMEZONE)
    scheduler = AsyncIOScheduler(timezone=tz)

    scheduler.add_job(
        report_service.send_periodic_summary,
        trigger=IntervalTrigger(minutes=REPORT_INTERVAL_MINUTES, timezone=tz),
        args=[bot, REPORT_INTERVAL_MINUTES],
        id="periodic_admin_report",
        replace_existing=True,
    )
    scheduler.start()
    return scheduler
