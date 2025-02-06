from time import time

from sqlalchemy import select

from bilibili_modles.Video import Video
from database import async_session
from nine_vocal_rank.db_models import (
    VideoSortedByVrankScore,
    VideoSortedByIncreaseView,
    FreshAchievementVideo,
)
from nine_vocal_rank.db_models.MonitoredVideo import MonitoredVideo


def video_to_monitored_video(video: Video):
    view = video.video_stat["view"]
    return MonitoredVideo(view=view, bvid=video.video_id["bvid"])


async def get_all_fresh_achievement_videos():
    async with async_session() as session:
        sql = select(FreshAchievementVideo).where()
        result = await session.scalars(sql)
        return result.all()


def monitored_video_to_fresh_achievement_video(video: MonitoredVideo):
    return FreshAchievementVideo(bvid=video.bvid, view=video.view, timestamp=time())


async def get_video_ranking(video: Video) -> tuple[int, int]:
    """
    获取视频排名
    :param video: 视频
    :return: (周刊得分排名， 视频播放量增长排名)
    """
    async with async_session() as session:
        sql = select(VideoSortedByVrankScore).where(
            VideoSortedByVrankScore.bvid == video.video_id["bvid"]
        )
        results = await session.scalars(sql)
        results = results.all()
        if len(results) == 0:
            score_rank = 0
        else:
            video_vrank_score_rank: VideoSortedByVrankScore = results[0]
            score_rank = video_vrank_score_rank.rank
        sql = select(VideoSortedByIncreaseView).where(
            VideoSortedByIncreaseView.bvid == video.video_id["bvid"]
        )
        results = await session.scalars(sql)
        results = results.all()
        if len(results) == 0:
            view_rank = 0
        else:
            video_increase_view_rank: VideoSortedByIncreaseView = results[0]
            view_rank = video_increase_view_rank.rank
        return score_rank, view_rank
