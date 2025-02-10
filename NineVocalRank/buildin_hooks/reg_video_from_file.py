import asyncio
import os
import random
from pathlib import Path

from bilibili_modles.Video import Video
from config import get_config, get_config_from_file, get_filter
from database.utils.add_video import add_video_to_db
from logger import logger
from nine_vocal_rank.exceptions.database import VideoValidationError

bvids = list()
lock = asyncio.Lock()
path = Path(get_config_from_file()["config"]["reg_from_file"]["path"])


async def get_bvid():
    global path
    global bvids
    count = len(bvids)
    while True:
        async with lock:
            if len(bvids) == 0:
                return
            item = bvids[0]
            bvids.remove(item)
            yield count - len(bvids), item
            if len(bvids) == 0:
                os.remove(path)
                return


async def reg_video_from_file():
    global bvids
    bvids = list()
    try:
        with open(path, "r", encoding="utf8") as f:
            bvids = f.read().split("\n")
    except FileNotFoundError:
        logger.info("没有找到批量导入文件...")
        return
    enable = get_config()["basic_config"]["spyder"]["async"]["enable"]
    task_count = get_config()["basic_config"]["spyder"]["async"]["task_count"]
    logger.info(f"准备从文件批量导入....[启动多任务：{task_count if enable else 0}]")
    if enable:
        for k in range(task_count):
            logger.debug(f"任务{k}启动")
            asyncio.get_event_loop().create_task(_reg_video_from_file(k))
    else:
        await _reg_video_from_file(0)


async def _reg_video_from_file(task_id):
    filter_ = get_filter()
    global bvids
    rand_min = get_config()["basic_config"]["spyder"]["sleep_min"]
    rand_max = get_config()["basic_config"]["spyder"]["sleep_max"]
    total = len(bvids)
    async for index, bvid in get_bvid():
        try:
            video = Video(bvid)
            await video.async_update_basic_data()
            flag, reason = await filter_.check(video)
            if flag:
                await add_video_to_db(video)
                logger.info(
                    f"[{index + 1}|{total}|{round(((index + 1) / total) * 100, 2)}%]成功导入：{video.video_info["title"]}({bvid})"
                )
            else:
                raise VideoValidationError(f"视频不符合收录规则！原因：{reason}")
        except Exception as e:
            logger.error(f"导入{bvid}时出现了异常！{type(e)}:{e.args}")
        await asyncio.sleep(random.uniform(rand_min, rand_max))
    logger.debug(f"任务{task_id}结束")
