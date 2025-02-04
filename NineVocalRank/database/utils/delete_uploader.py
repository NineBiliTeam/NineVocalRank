from sqlalchemy import select

from bilibili_modles.Uploader import Uploader
from database import async_session
from database.model.Uploader import UploaderDB


async def delete_uploader(uploader_: Uploader):
    async with async_session() as session:
        sql = select(UploaderDB).where(UploaderDB.mid == uploader_.mid)
        uploader = await session.scalars(sql)
        uploader = uploader.all()[0]
        await session.delete(uploader)
        await session.commit()
