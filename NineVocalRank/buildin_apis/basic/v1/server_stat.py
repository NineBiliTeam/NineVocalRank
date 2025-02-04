import time

from fastapi import APIRouter
from pydantic import BaseModel, Field

server_stat_router = APIRouter(prefix="/ServerStat", tags=["Server"])


class ServerStat(BaseModel):
    timestamp: int = Field(title="服务器当前UNIX时间戳")


@server_stat_router.get("/info")
async def get_server_stat() -> ServerStat:
    """获取服务器的性能等基本信息"""
    return ServerStat(
        timestamp=int(time.time()),
    )
