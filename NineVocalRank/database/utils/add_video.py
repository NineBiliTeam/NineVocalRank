from sqlalchemy import select

from bilibili_modles.Uploader import Uploader
from bilibili_modles.Video import Video
from database import async_session
from database.model.Video import VideoDB
from database.utils.add_uploader import add_uploader_to_db
from utils.to_models import video_model_to_db


async def add_video_to_db(video: Video):
    async with async_session() as session:
        sql = select(VideoDB).where(VideoDB.bvid == video.video_id["bvid"])
        data = await session.scalars(sql)
        if len(data.all()) != 0:
            return
        video_db = video_model_to_db(video)
        session.add(video_db)
        await session.commit()
    uploader = Uploader(video.video_info["uploader_mid"])
    await uploader.async_update_basic_data()
    await add_uploader_to_db(uploader)
