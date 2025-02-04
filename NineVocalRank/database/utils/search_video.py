from sqlalchemy import select

from bilibili_modles.Video import Video
from database.model.Video import VideoDB
from database.utils import search_by_sql
from utils.to_schemas import video_db_to_model


def make_video_model_list_from_db_list(raw: list[VideoDB] | VideoDB):
    return [video_db_to_model(video) for video in raw]


async def search_video_by_bvid(bvid) -> list[Video]:
    sql = select(VideoDB).where(VideoDB.bvid == bvid)
    result = await search_by_sql(sql)
    return make_video_model_list_from_db_list(result)


async def search_video_by_avid(avid) -> list[Video]:
    sql = select(VideoDB).where(VideoDB.avid == avid)
    result = await search_by_sql(sql)
    return make_video_model_list_from_db_list(result)


async def search_video_by_title_keyword(title_keyword) -> list[Video]:
    sql = select(VideoDB).where(VideoDB.title.like(f"%{title_keyword}%"))
    result = await search_by_sql(sql)
    return make_video_model_list_from_db_list(result)
