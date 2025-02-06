from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.params import Path
from pydantic import BaseModel, Field

from bilibili_modles.Uploader import Uploader
from database.utils.search_uploader import (
    search_uploader_by_mid,
    search_uploader_by_name_keyword,
)

uploader_router = APIRouter(prefix="/uploader", tags=["Uploader"])


@uploader_router.get("/{mid}/get_stat")
async def get_stat(mid: Annotated[str, Path(title="UP主的mid")]) -> Uploader:
    """
    获取一个UP主的状态信息.
    此处获得的对象为NineBiliRank内部处理UP自己数据的对象.
    """
    uploader = Uploader(mid=mid)
    await uploader.async_update_basic_data()
    return uploader


@uploader_router.get("/search_from_db")
async def search_from_db(
    mid: int | None = Query(default=None, title="UP主mid"),
    name: str | None = Query(default=None, title="up主名字关键字词"),
) -> list[Uploader]:
    """
    从数据库查询UP主数据.
    不是最新数据，而是数据库收录时的数据
    如果存在多个查询参数，则按照mid->name的顺序，查询存在的最高优先级的关键词
    如果查询参数全部没有，则返回空列表
    :param mid: UP主mid
    :param name: UP主名字关键词
    :return:
    """
    if mid is not None:
        result = await search_uploader_by_mid(mid)
        return result
    if name is not None:
        result = await search_uploader_by_name_keyword(name)
        return result
    return []
