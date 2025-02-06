from fastapi import APIRouter
from pydantic import BaseModel, Field

from database.model.Uploader import UploaderDB
from database.model.Video import VideoDB

database_router = APIRouter(
    prefix="/database",
    tags=["Database"],
)


class Count(BaseModel):
    count: int = Field(default=0, title="表内数据数量")


@database_router.get("/video_count")
async def get_video_count() -> Count:
    """
    获取数据库内视频数量
    :return:
    """
    return Count(count=await VideoDB.count())


@database_router.get("/uploader_count")
async def get_video_count() -> Count:
    """
    获取数据库内UP主数量
    :return:
    """
    return Count(count=await UploaderDB.count())
