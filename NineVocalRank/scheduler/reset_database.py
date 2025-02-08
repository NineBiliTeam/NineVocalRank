import asyncio
import random

from bilibili_modles.Uploader import Uploader
from bilibili_modles.Video import Video
from config import get_config, get_config_from_file
from database import async_session
from database.model.Uploader import UploaderDB
from database.model.Video import VideoDB
from database.utils.update_uploader import update_uploader
from database.utils.update_video import update_video
from logger import logger

lock = asyncio.Lock()

nbid = 0
nbuid = 0
async def _get_nbid():
    global nbid
    while True:
        async with lock:
            nbid+=1
            yield nbid

async def _get_nbuid():
    global nbuid
    while True:
        async with lock:
            nbuid+=1
            yield nbuid

async def reset_database():
    global nbid, nbuid
    nbid = 0
    nbuid = 0
    enable = get_config_from_file()["basic_config"]["spyder"]["async"]["enable"]
    task_count = get_config_from_file()["basic_config"]["spyder"]["async"]["task_count"]
    if enable:
        for i in range(task_count):
            logger.info(f"启动任务{i}")
            asyncio.get_event_loop().create_task(_reset_database(i))
    else:
        await _reset_database(0)

async def _reset_database(task_id:int):
    rand_min = get_config()["basic_config"]["spyder"]["sleep_min"]
    rand_max = get_config()["basic_config"]["spyder"]["sleep_max"]
    max_ = await VideoDB.max_id()
    # 重置视频
    total = await VideoDB.count()
    for _ in range(total):
        while True:
            i = await _get_nbid().__anext__()
            async with async_session(autoflush=True) as session:
                from sqlalchemy import select
                sql = select(VideoDB).where(VideoDB.nbid == i)
                result = await session.scalars(sql)
                result = result.all()
                if i > max_:
                    break
                if len(result) == 0:
                    continue

            video_db: VideoDB = result[0]
            try:
                video = Video(video_db.bvid)
                await video.async_update_basic_data()
                await update_video(video)
                logger.info(f"[{task_id}]成功重置：{video_db.bvid}")
            except Exception as e:
                logger.error(f"出现异常{type(e)}:{e.args}")
            await asyncio.sleep(random.uniform(rand_min, rand_max))
            break
    # 重置UP主
    total = await UploaderDB.count()
    max_ = await UploaderDB.max_id()
    for _ in range(total):
        while True:
            i = await _get_nbuid().__anext__()
            async with async_session(autoflush=True) as session:
                from sqlalchemy import select

                sql = select(UploaderDB).where(UploaderDB.nbuid == i)
                result = await session.scalars(sql)
                result = result.all()
                if i > max_:
                    break
                if len(result) == 0:
                    continue

            uploader_db: UploaderDB = result[0]
            try:
                uploader = Uploader(uploader_db.mid)
                await uploader.async_update_basic_data()
                await update_uploader(uploader)
                logger.info(f"[{task_id}]成功重置{uploader_db.mid}")
            except Exception as e:
                logger.error(f"出现异常{type(e)}:{e.args}")
            await asyncio.sleep(random.uniform(rand_min, rand_max))
            break
    logger.info(f"[{task_id}]本协程数据全部重置完成")
