from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Query, Path

from bilibili_modles.Video import Video
from buildin_apis.basic.v1.models import VideoIDRequestModel
from database.utils.search_video import (
    search_video_by_bvid,
    search_video_by_avid,
    search_video_by_title_keyword,
)

video_router = APIRouter(prefix="/video", tags=["Video"])


@video_router.get("/{vid}")
async def get_stat(vid: Annotated[str, Path(title="视频ID，支持AVID与BVID")]) -> Video:
    """
    获取视频的当前数据.
    此处获取的Video对象为NineBiliRank处理视频的对象
    """
    video = Video(video_id=vid)
    await video.async_update_basic_data()
    return video


@video_router.get("/search_from_db")
async def search_from_db(
    bvid: str | None = Query(default=None, title="视频BV号"),
    avid: str | None = Query(default=None, title="视频AV号"),
    title: str | None = Query(default=None, title="视频标题关键词"),
) -> list[Video]:
    """
    从数据库查询视频数据.
    不是最新数据，而是数据库收录时的数据
    如果存在多个查询参数，则按照bvid->avid->title的顺序，查询存在的最高优先级的关键词
    如果三个查询参数全部没有，则返回空列表
    :param bvid:视频的BV号
    :param avid:视频的AV号
    :param title:视频的标题
    :return:
    """
    if bvid is not None:
        result = await search_video_by_bvid(bvid)
        return result
    if avid is not None:
        result = await search_video_by_avid(avid.lower().replace("av", ""))
        return result
    if title is not None:
        result = await search_video_by_title_keyword(title)
        return result
    return []
