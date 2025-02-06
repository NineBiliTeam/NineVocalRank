from sqlalchemy import Column, Integer, String, func, select
from sqlalchemy.orm import Mapped

from database import async_session
from database.Base import Base


class VideoSortedByIncreaseView(Base):
    __tablename__ = "video_sorted_by_increase_view"

    rank: Mapped[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    view: Mapped[int] = Column(Integer, nullable=False)
    bvid: Mapped[str] = Column(String(32), nullable=False)

    @staticmethod
    async def count():
        sql = select(func.count(VideoSortedByIncreaseView.rank))
        async with async_session() as session:
            return await session.scalar(sql)


class VideoSortedByVrankScore(Base):
    __tablename__ = "video_sorted_by_vrank_score"

    rank: Mapped[int] = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    score: Mapped[int] = Column(Integer, nullable=False)
    bvid: Mapped[str] = Column(String(32), nullable=False)

    @staticmethod
    async def count():
        sql = select(func.count(VideoSortedByVrankScore.rank))
        async with async_session() as session:
            return await session.scalar(sql)
