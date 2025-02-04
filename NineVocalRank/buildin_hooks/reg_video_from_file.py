import asyncio
import os
import random
from pathlib import Path

from StartUp import reg_start_hooks
from bilibili_modles.Video import Video
from config import get_config
from database.utils.add_video import add_video_to_db
from logger import logger


async def reg_video_from_file():
    rand_min = get_config()["basic_config"]["spyder"]["sleep_min"]
    rand_max = get_config()["basic_config"]["spyder"]["sleep_max"]
    path = Path(get_config()["config"]["reg_from_file"]["path"])
    logger.info(f"批量导入文件路径：{path}")
    try:
        with open(path, "r", encoding="utf8") as f:
            bvids = f.read().split("\n")
    except FileNotFoundError:
        logger.info("没有找到批量导入文件...")
        return
    total = len(bvids)
    for index, bvid in enumerate(bvids):
        try:
            video = Video(bvid)
            await video.async_update_basic_data()
            await add_video_to_db(video)
            logger.info(
                f"[{index + 1}|{total}|{round(((index + 1) / total) * 100, 2)}%]成功导入：{video.video_info["title"]}({bvid})"
            )
        except Exception as e:
            logger.error(f"导入{bvid}时出现了异常！{type(e)}:{e.args}")
        await asyncio.sleep(random.uniform(rand_min, rand_max))
    os.remove(path)
    logger.success("批量导入完成，已经删除文件...")


reg_start_hooks(reg_video_from_file)
