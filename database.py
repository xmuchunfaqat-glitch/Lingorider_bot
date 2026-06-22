"""
Ma'lumotlar bazasi — modellar va so'rovlar (CRUD) bitta faylda (SQLite, async SQLAlchemy).
"""
import os
from datetime import datetime, timedelta

from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Boolean, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import DB_PATH


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    region: Mapped[str] = mapped_column(String(100), nullable=True)
    district: Mapped[str] = mapped_column(String(150), nullable=True)
    goal: Mapped[str] = mapped_column(String(200), nullable=True)
    target_language: Mapped[str] = mapped_column(String(50), nullable=True)
    daily_routine: Mapped[str] = mapped_column(String(300), nullable=True)
    focus_area: Mapped[str] = mapped_column(String(100), nullable=True)

    onboarding_complete: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_active: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    exercises: Mapped[list["ExerciseLog"]] = relationship(back_populates="user")


class ExerciseLog(Base):
    __tablename__ = "exercise_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    language: Mapped[str] = mapped_column(String(50))
    target_text: Mapped[str] = mapped_column(String(300))
    heard_text: Mapped[str] = mapped_column(String(300), nullable=True)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="exercises")


class ReportLog(Base):
    """Adminga yuborilgan har bir hisobotni qayd qilish (takror yubormaslik uchun)."""
    __tablename__ = "report_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    report_type: Mapped[str] = mapped_column(String(50))
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}", echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_or_create_user(telegram_id: int) -> User:
    async with async_session() as session:
        user = await session.get(User, telegram_id)
        if user is None:
            user = User(telegram_id=telegram_id)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user


async def update_user(telegram_id: int, **fields) -> User:
    async with async_session() as session:
        user = await session.get(User, telegram_id)
        if user is None:
            user = User(telegram_id=telegram_id)
            session.add(user)
        for key, value in fields.items():
            setattr(user, key, value)
        user.last_active = datetime.utcnow()
        await session.commit()
        await session.refresh(user)
        return user


async def get_user(telegram_id: int):
    async with async_session() as session:
        return await session.get(User, telegram_id)


async def log_exercise(user_id: int, language: str, target_text: str,
                        heard_text: str, score: float, is_correct: bool) -> ExerciseLog:
    async with async_session() as session:
        entry = ExerciseLog(
            user_id=user_id, language=language, target_text=target_text,
            heard_text=heard_text, score=score, is_correct=is_correct,
        )
        session.add(entry)
        await session.commit()
        await session.refresh(entry)
        return entry


async def get_user_stats(user_id: int) -> dict:
    async with async_session() as session:
        result = await session.execute(
            select(func.count(ExerciseLog.id), func.avg(ExerciseLog.score))
            .where(ExerciseLog.user_id == user_id)
        )
        total, avg_score = result.one()
        last = await session.execute(
            select(ExerciseLog.created_at)
            .where(ExerciseLog.user_id == user_id)
            .order_by(ExerciseLog.created_at.desc())
            .limit(1)
        )
        last_date = last.scalar()
        return {
            "total": total or 0,
            "avg_score": round(avg_score or 0, 1),
            "last_date": last_date.strftime("%Y-%m-%d %H:%M") if last_date else "—",
        }


async def get_activity_since(minutes: int) -> dict:
    """So'nggi N daqiqadagi yangi foydalanuvchilar va bajarilgan mashqlar."""
    since = datetime.utcnow() - timedelta(minutes=minutes)
    async with async_session() as session:
        new_users = await session.execute(
            select(func.count(User.telegram_id)).where(User.created_at >= since)
        )
        new_exercises = await session.execute(
            select(func.count(ExerciseLog.id)).where(ExerciseLog.created_at >= since)
        )
        avg_score = await session.execute(
            select(func.avg(ExerciseLog.score)).where(ExerciseLog.created_at >= since)
        )
        return {
            "new_users": new_users.scalar() or 0,
            "new_exercises": new_exercises.scalar() or 0,
            "avg_score": round(avg_score.scalar() or 0, 1),
        }


async def get_total_counts() -> dict:
    async with async_session() as session:
        total_users = await session.execute(select(func.count(User.telegram_id)))
        total_exercises = await session.execute(select(func.count(ExerciseLog.id)))
        return {
            "total_users": total_users.scalar() or 0,
            "total_exercises": total_exercises.scalar() or 0,
        }


async def mark_report_sent(report_type: str):
    async with async_session() as session:
        session.add(ReportLog(report_type=report_type))
        await session.commit()
