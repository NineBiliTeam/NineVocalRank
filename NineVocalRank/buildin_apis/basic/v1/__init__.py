from fastapi import APIRouter

from buildin_apis.basic.v1.database import database_router
from buildin_apis.basic.v1.server_stat import server_stat_router
from buildin_apis.basic.v1.uploader_datas import uploader_router
from buildin_apis.basic.v1.uploader_manager import uploader_manager_router
from buildin_apis.basic.v1.video_datas import video_router
from buildin_apis.basic.v1.video_manage import video_manager_router
from buildin_apis.models import APIPluginMeta

basic_v1_router = APIRouter(
    prefix="/basic/v1",
    tags=["BASIC V1"],
)


@basic_v1_router.get("/")
async def root() -> APIPluginMeta:
    return APIPluginMeta(
        name="basic_api",
        version="1.0.0",
        description="NineBiliRank的基础功能API",
        plugin_type="buildin",
        author="Moran0710",
    )


basic_v1_router.include_router(server_stat_router)
basic_v1_router.include_router(uploader_router)
basic_v1_router.include_router(video_router)
basic_v1_router.include_router(video_manager_router)
basic_v1_router.include_router(uploader_manager_router)
basic_v1_router.include_router(database_router)
