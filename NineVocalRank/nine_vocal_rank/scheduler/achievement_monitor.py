from tabnanny import check

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from logger import logger
from bilibili_modles.Video import Video
from config import get_config_from_file
from database import async_session
from nine_vocal_rank.db_models import MonitoredVideo, FreshAchievementVideo
from nine_vocal_rank.models.VocaloidVideo import VocaloidVideo
from nine_vocal_rank.models.enums import VideoRankCode
from nine_vocal_rank.utils.db import monitored_video_to_fresh_achievement_video
from nine_vocal_rank.utils.vrank_score import get_target_view

level_5 = get_config_from_file()["config"]["vrank_monitor"]["level_5"]
level_4 = get_config_from_file()["config"]["vrank_monitor"]["level_4"]
level_3 = get_config_from_file()["config"]["vrank_monitor"]["level_3"]
level_2 = get_config_from_file()["config"]["vrank_monitor"]["level_2"]
level_1 = get_config_from_file()["config"]["vrank_monitor"]["level_1"]

async def check_video(video:MonitoredVideo,level:int, session:AsyncSession):
    target_view = get_target_view(video.view)
    difference = target_view - video.view
    for level_code, level_view in (
            (5, level_5), (4, level_4), (3, level_3), (2, level_2), (1, level_1)
    ):
        if difference <= level_view and level == level_code:
            await upgrade_video(target_view, video, session)

async def upgrade_video(target_view, monitored_video:MonitoredVideo, session:AsyncSession):
    video = VocaloidVideo(Video(monitored_video.bvid))
    await video.async_update_basic_data()
    monitored_video.view = video.video_stat["view"]
    difference = target_view - video.video_stat["view"]
    if difference <= 0:
        fresh_video = monitored_video_to_fresh_achievement_video(monitored_video)
        session.add(fresh_video)
        await session.delete(monitored_video)
        logger.info(f"{video.video_id["bvid"]}达成成就：{target_view}")
    else:
        logger.info(f"目前视频{video.video_id["bvid"]}还差{difference}达到{target_view}")


async def achievement_monitor(level:int):
    count = await MonitoredVideo.count()
    i = 0
    max_ = await MonitoredVideo.max_id()
    if level==2:
        logger.info("正在清空最新达成成就的歌曲的数据...")
        async with async_session() as session:
            sql = select(FreshAchievementVideo).where()
            videos = await session.scalars(sql)
            videos = videos.all()
            for video in videos:
                await session.delete(video)
            await session.commit()
    for _ in range(count):
        while True:
            i+=1
            async with async_session() as session:
                sql = select(MonitoredVideo).where(MonitoredVideo.id == i)
                monitored_videos = await session.scalars(sql)
                monitored_videos = monitored_videos.all()
                if i > max_:
                    break
                if len(monitored_videos) == 0:
                    continue
                monitored_video = monitored_videos[0]
                await check_video(monitored_video, level, session)
                await session.commit()
