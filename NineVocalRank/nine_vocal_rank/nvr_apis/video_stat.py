from fastapi import APIRouter
from fastapi.params import Query, Path
from typing_extensions import Annotated

from logger import logger
from bilibili_modles.Video import Video
from nine_vocal_rank.models.VocaloidVideo import VocaloidVideo

video_stat_router = APIRouter(
    prefix="/video",
    tags=["Video"],
)


@video_stat_router.get("/{vid}")
async def get_video(
    vid: Annotated[str, Path(title="视频ID，支持AVID与BVID")],
) -> VocaloidVideo:
    """
    以Vocaloid形式获取视频信息
    比起BASIC模块，多出VOCALOID相关数据
    未注册的视频，如果识别为符合NBVC规则的曲目，则会自动注册，返回的周刊得分等数据恒为0
    如果请求的视频不是符合NBVC规则的曲目，则抛出VideoValidationError
    """
    video: VocaloidVideo = VocaloidVideo(vid)
    await video.async_update_basic_data()
    return video

