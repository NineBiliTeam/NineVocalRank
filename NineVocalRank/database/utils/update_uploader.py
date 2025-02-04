import time

from sqlalchemy import select

from bilibili_modles.Uploader import Uploader
from database import async_session
from database.model.Uploader import UploaderDB


async def update_uploader(uploader: Uploader):
    async with async_session() as session:
        sql = select(UploaderDB).where(Uploader == uploader.mid)
        result = await session.scalars(sql)
        result = result.all()
        if len(result) == 0:
            return

        uploader_db: UploaderDB = result[0]
        uploader_db.mid = uploader.mid
        uploader_db.archive_count = uploader.archive_count
        uploader_db.name = uploader.name
        uploader_db.fans = uploader.fans
        uploader_db.timestamp = int(time.time())
        await session.commit()
