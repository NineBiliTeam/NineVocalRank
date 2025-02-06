from sqlalchemy import Column, Integer, Float, String, select, func
from sqlalchemy.orm import Mapped

from database import Base, async_session


class MonitoredVideo(Base):
    __tablename__ = "monitored_video"
    id: Mapped[int] = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    view: Mapped[int] = Column(Integer, nullable=False)
    bvid: Mapped[str] = Column(String(32), nullable=False)

    @staticmethod
    async def count():
        sql = select(func.count(MonitoredVideo.id))
        async with async_session() as session:
            return await session.scalar(sql)

    @staticmethod
    async def max_id():
        sql = select(func.max(MonitoredVideo.id))
        async with async_session() as session:
            return await session.scalar(sql)


class FreshAchievementVideo(Base):
    __tablename__ = "fresh_achievement_video"
    id: Mapped[int] = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    view: Mapped[int] = Column(Integer, nullable=False)
    bvid: Mapped[str] = Column(String(32), nullable=False)
    timestamp: Mapped[float] = Column(Float, nullable=False)

    @staticmethod
    async def count():
        sql = select(func.count(FreshAchievementVideo.id))
        async with async_session() as session:
            return await session.scalar(sql)

    @staticmethod
    async def max_id():
        sql = select(func.max(FreshAchievementVideo.id))
        async with async_session() as session:
            return await session.scalar(sql)
