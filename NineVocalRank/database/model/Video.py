from sqlalchemy import Column, Integer, String, select, func
from sqlalchemy.dialects.postgresql import asyncpg
from sqlalchemy.orm import Mapped

from database import Base, async_session


class VideoDB(Base):
    __tablename__ = "Video"

    # ---------------基本数据-----------------
    view: Mapped[int] = Column(Integer, nullable=False)
    like: Mapped[int] = Column(Integer, nullable=False)
    coin: Mapped[int] = Column(Integer, nullable=False)
    favorite: Mapped[int] = Column(Integer, nullable=False)
    reply: Mapped[int] = Column(Integer, nullable=False)
    share: Mapped[int] = Column(Integer, nullable=False)
    danmaku: Mapped[int] = Column(Integer, nullable=False)

    # --------------视频特征-----------------
    uploader_mid: Mapped[str] = Column(String(32), nullable=False)
    title: Mapped[str] = Column(String(128), nullable=False)
    avid: Mapped[str] = Column(String(64), nullable=False)
    bvid: Mapped[str] = Column(String(64), nullable=False)
    tid: Mapped[int] = Column(Integer, nullable=False)
    timestamp: Mapped[int] = Column(Integer, nullable=False)

    # --------------------其他-------------------
    pic: Mapped[str] = Column(String(256), nullable=False)
    pages: Mapped[int] = Column(Integer, nullable=False)
    nbid: Mapped[int] = Column(
        Integer, autoincrement=True, nullable=False, primary_key=True
    )

    @staticmethod
    async def count():
        sql = select(func.count(VideoDB.nbid))
        async with async_session() as session:
            return await session.scalar(sql)

    @staticmethod
    async def max_id():
        sql = select(func.max(VideoDB.nbid))
        async with async_session() as session:
            return await session.scalar(sql)
