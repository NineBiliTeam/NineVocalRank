from sqlalchemy import select

from bilibili_modles.Video import Video
from database import async_session
from database.model.Video import VideoDB


async def delete_video(video_: Video):
    async with async_session() as session:
        sql = select(VideoDB).where(VideoDB.bvid == video_.video_id["bvid"])
        video = await session.scalars(sql)
        video = video.all()[0]
        await session.delete(video)
        await session.commit()
