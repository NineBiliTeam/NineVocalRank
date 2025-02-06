import asyncio
import random

from bilibili_modles.Uploader import Uploader
from bilibili_modles.Video import Video
from config import get_config
from database import async_session
from database.model.Uploader import UploaderDB
from database.model.Video import VideoDB
from database.utils.update_uploader import update_uploader
from database.utils.update_video import update_video
from logger import logger


async def reset_database():
    rand_min = get_config()["basic_config"]["spyder"]["sleep_min"]
    rand_max = get_config()["basic_config"]["spyder"]["sleep_max"]
    logger.info("正在重置视频")
    max_ = await VideoDB.max_id()
    i = 0
    # 重置视频
    total = await VideoDB.count()
    for _ in range(total):
        while True:
            i += 1
            async with async_session() as session:
                from sqlalchemy import select

                sql = select(VideoDB).where(VideoDB.nbid == i)
                result = await session.scalars(sql)
                result = result.all()
                if len(result) == 0:
                    continue
                if i > max_:
                    break

            video_db: VideoDB = result[0]
            try:
                video = Video(video_db.bvid)
                await video.async_update_basic_data()
                await update_video(video)
            except Exception as e:
                logger.error(f"出现异常{type(e)}:{e.args}")
            await asyncio.sleep(random.uniform(rand_min, rand_max))
            break

    logger.info("视频数据重置完成")
    i = 0
    # 重置UP主
    total = await UploaderDB.count()
    for _ in range(total):
        while True:
            i += 1
            async with async_session() as session:
                from sqlalchemy import select

                sql = select(UploaderDB).where(UploaderDB.nbuid == i)
                result = await session.scalars(sql)
                result = result.all()
                if len(result) == 0:
                    continue

            uploader_db: UploaderDB = result[0]
            try:
                uploader = Uploader(uploader_db.mid)
                await uploader.async_update_basic_data()
                await update_uploader(uploader)
            except Exception as e:
                logger.error(f"出现异常{type(e)}:{e.args}")
            await asyncio.sleep(random.uniform(rand_min, rand_max))
            break
    logger.success("数据库重置全部完成")
