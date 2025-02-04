import time

from sqlalchemy import select

from bilibili_modles.Video import Video
from database import async_session
from database.model.Video import VideoDB


async def update_video(video: Video):
    async with async_session() as session:
        sql = select(VideoDB).where(VideoDB.bvid == video.video_id["bvid"])
        result = await session.scalars(sql)
        video_db = result.all()
        if len(video_db) == 0:
            return
        video_db = video_db[0]
        video_db.bvid = video.video_id["bvid"]
        video_db.avid = video.video_id["avid"]
        video_db.tid = video.video_id["tid"]

        video_db.view = video.video_stat["view"]
        video_db.like = video.video_stat["like"]
        video_db.coin = video.video_stat["coin"]
        video_db.favorite = video.video_stat["favorite"]
        video_db.share = video.video_stat["share"]
        video_db.reply = video.video_stat["reply"]
        video_db.danmaku = video.video_stat["danmaku"]

        video_db.uploader_mid = video.video_info["uploader_mid"]
        video_db.pages = video.video_info["pages"]
        video_db.pic = video.video_info["pic"]
        video_db.title = video.video_info["title"]
        video_db.timestamp = int(time.time())

        await session.commit()
