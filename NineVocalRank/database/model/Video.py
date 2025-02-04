from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped

from database import Base


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
    uploader_mid: Mapped[int] = Column(Integer, nullable=False)
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
