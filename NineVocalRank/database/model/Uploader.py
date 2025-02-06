from sqlalchemy import Column, Integer, String, func, select
from sqlalchemy.orm import Mapped

from bilibili_modles.Uploader import Uploader
from database import Base, async_session


class UploaderDB(Base):
    __tablename__ = "uploader"

    mid: Mapped[str] = Column(String(32), nullable=False)
    name: Mapped[str] = Column(String(64), nullable=False)
    fans: Mapped[int] = Column(Integer, nullable=False)
    archive_count: Mapped[int] = Column(Integer, nullable=False)
    nbuid: Mapped[str] = Column(
        Integer, nullable=False, autoincrement=True, primary_key=True
    )
    timestamp: Mapped[int] = Column(Integer, nullable=False)

    @staticmethod
    async def count():
        sql = select(func.count(UploaderDB.nbuid))
        async with async_session() as session:
            return await session.scalar(sql)

    @staticmethod
    async def max_id():
        sql = select(func.max(UploaderDB.nbuid))
        async with async_session() as session:
            return await session.scalar(sql)
