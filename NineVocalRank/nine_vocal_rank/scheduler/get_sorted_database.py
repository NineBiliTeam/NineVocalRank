import asyncio
from collections import namedtuple
import random

from logger import logger
from bilibili_modles.Video import Video
from config import get_config, get_config_from_file
from database import async_session
from database.model.Video import VideoDB
from nine_vocal_rank.db_models import VideoSortedByVrankScore, VideoSortedByIncreaseView
from nine_vocal_rank.models.VocaloidVideo import VocaloidVideo
from nine_vocal_rank.utils.db import video_to_monitored_video
from nine_vocal_rank.utils.vrank_score import get_target_view
from utils.math_utils import calculate_percentage

VideoTuple = namedtuple("VideoTuple", ["bvid", "increase_view", "score"])
level_5 = get_config_from_file()["config"]["vrank_monitor"]["level_5"]


async def get_sorted_database():
    logger.info("正在爬取数据...")
    videos = await get_video_tuples()
    logger.info("数据爬取完成，正在清空数据库...")
    await clean_score_database()
    logger.info("数据清空完成，添加数据...")
    await add_videos_rank_to_database(videos)
    logger.success("排名数据添加完成")


async def add_videos_rank_to_database(videos: list[VideoTuple]):
    videos = sorted(videos, key=lambda v: v.increase_view, reverse=True)
    for video in videos:
        async with async_session() as session:
            session.add(
                VideoSortedByIncreaseView(
                    bvid=video.bvid,
                    view=video.increase_view,
                )
            )
            await session.commit()

    videos = sorted(videos, key=lambda v: v.score, reverse=True)
    for video in videos:
        async with async_session() as session:
            session.add(
                VideoSortedByVrankScore(
                    bvid=video.bvid,
                    score=video.score,
                )
            )
            await session.commit()


async def get_video_tuples() -> list[VideoTuple]:
    videos: list[VideoTuple] = list()
    total = await VideoDB.count()
    i = 0
    rand_min = get_config()["basic_config"]["spyder"]["sleep_min"]
    rand_max = get_config()["basic_config"]["spyder"]["sleep_max"]
    max_ = await VideoDB.max_id()
    for k in range(total):
        while True:
            i += 1
            async with async_session() as session:
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
                    video = VocaloidVideo(Video(video_db.bvid))
                    await video.async_update_basic_data()
                    target_view = get_target_view(video.video_stat["view"])
                    difference = target_view - video.video_stat["view"]
                    if difference <= level_5:
                        logger.info(
                            f"发现视频{video.video_id["bvid"]}还差{level_5}播放达成下一成绩({difference})，已经加入监测"
                        )
                        session.add(video_to_monitored_video(video))
                    videos.append(
                        VideoTuple(
                            video.video_id["bvid"],
                            video.video_increase["view"],
                            video.vrank_info["vrank_score"],
                        )
                    )
                    logger.info(
                        f"[{k} | {total} | {calculate_percentage(k, total)}%]成功加入{video_db.bvid}"
                    )
                except Exception as e:
                    logger.error(f"出现异常{type(e)}:{e.args}")
                await asyncio.sleep(random.uniform(rand_min, rand_max))
                await session.commit()
                break

    return videos


async def clean_score_database():
    total = await VideoSortedByVrankScore.count()
    i = 0
    for _ in range(total):
        while True:
            i += 1
            async with async_session() as session:
                from sqlalchemy import select

                sql = select(VideoSortedByVrankScore).where(
                    VideoSortedByVrankScore.rank == i
                )
                result = await session.scalars(sql)
                result = result.all()
                if len(result) == 0:
                    continue
                result = result[0]
                await session.delete(result)
                await session.commit()
                break
    logger.info("已经清空VideoSortedByVrankScore")

    total = await VideoSortedByIncreaseView.count()
    i = 0
    for _ in range(total):
        while True:
            i += 1
            async with async_session() as session:
                from sqlalchemy import select

                sql = select(VideoSortedByIncreaseView).where(
                    VideoSortedByIncreaseView.rank == i
                )
                result = await session.scalars(sql)
                result = result.all()
                if len(result) == 0:
                    continue
                result = result[0]
                await session.delete(result)
                await session.commit()
                break
    logger.info("已经清空VideoSortedByIncreaseView")
