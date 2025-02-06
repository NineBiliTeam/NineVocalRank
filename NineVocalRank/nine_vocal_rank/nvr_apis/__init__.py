from fastapi import APIRouter

from NineVocalRank.buildin_apis.models import APIPluginMeta
from NineVocalRank.nine_vocal_rank.nvr_apis.video_stat import video_stat_router
from nine_vocal_rank.nvr_apis.video_monitor import monitor_router
from nine_vocal_rank.nvr_apis.vrank_sort import sorted_router

nine_vocal_rank_router = APIRouter(
    prefix="/vocaloid_rank/v1",
    tags=["Vocaloid"],
)


@nine_vocal_rank_router.get("/")
async def index():
    return APIPluginMeta(
        name="NineVocalRank",
        version="1.0.0",
        description="用于中文虚拟歌手曲目数据查询",
        plugin_type="rank",
        author="moran0710",
    )


nine_vocal_rank_router.include_router(video_stat_router)
nine_vocal_rank_router.include_router(sorted_router)
nine_vocal_rank_router.include_router(monitor_router)
