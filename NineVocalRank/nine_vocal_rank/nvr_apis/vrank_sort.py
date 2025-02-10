from typing import Annotated

from fastapi import APIRouter, Path
from pydantic import BaseModel, Field

from nine_vocal_rank.models.VocaloidVideo import VocaloidVideo
from nine_vocal_rank.utils.db import get_video_ranking

sorted_router = APIRouter(prefix="/sorted", tags=["Vocaloid"])


class RankingData(BaseModel):
    view_rank: int = Field(description="此视频增长播放在数据库内的排名")
    score_rank: int = Field(description="此视频周刊得分在数据库内的排名")


@sorted_router.get("/{vid}")
async def get_video_ranking_(
    vid: Annotated[str, Path(title="视频ID，支持AVID与BVID (AVID会慢很多)")],
) -> RankingData:
    """
    获取视频的排名
    """
    video = VocaloidVideo(vid)
    if video.video_id["bvid"] == "":
        await video.async_update_basic_data()

    score_rank, view_rank = await get_video_ranking(video)
    return RankingData(view_rank=view_rank, score_rank=score_rank)
