from sqlalchemy import select

from bilibili_modles.Uploader import Uploader
from database import async_session
from database.model.Uploader import UploaderDB
from utils.to_models import uploader_model_to_db


async def add_uploader_to_db(uploader: Uploader):
    sql = select(UploaderDB).where(UploaderDB.mid == uploader.mid)
    async with async_session() as session:
        result = await session.scalars(sql)
        if len(result.all()) != 0:
            return
        uploader_db = uploader_model_to_db(uploader)
        session.add(uploader_db)
        await session.commit()
