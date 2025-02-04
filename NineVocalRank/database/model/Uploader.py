from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped

from database import Base


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
