from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from bilibili_modles.Video import Video
from nine_vocal_rank.models.VocaloidVideo import VocaloidVideo
from nine_vocal_rank.utils.db import get_all_fresh_achievement_videos
from nine_vocal_rank.utils.vrank_score import get_rank

monitor_router = APIRouter(
    prefix="/video_monitor",
    tags=["Vocaloid"],
)


class VideoRank(TypedDict):
    timestamp: float
    video: VocaloidVideo


@monitor_router.get("/latest")
async def get_latest() -> list[VideoRank]:
    """
    获取最新的，达成一个成就的视频
    此接口可以获取到10分钟内达成某一个成就的视频，每10分钟刷新数据库
    """
    fresh_videos = await get_all_fresh_achievement_videos()
    result = list()
    for video in fresh_videos:
        vocaloid_video = VocaloidVideo(video.bvid)
        await vocaloid_video.async_update_basic_data()
        rank_code, rank_message, _ = get_rank(vocaloid_video.video_stat["view"])
        result.append(
            VideoRank(
                timestamp=video.timestamp,
                video=vocaloid_video,
            )
        )
    return result
