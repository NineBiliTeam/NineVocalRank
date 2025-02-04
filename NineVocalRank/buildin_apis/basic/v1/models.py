from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ResponseStatus(Enum):
    success = 0  # 视频合法
    video_is_invalid = -10100  # 视频不合法


class ResponseStatusMessage(Enum):
    success = "success"  # 视频合法
    video_is_invalid = "video is invalid."  # 视频不合法


class VideoIDRequestModel(BaseModel):
    vid: str = Field(title="视频ID，支持AVID与BVID，AVID需要有av前缀，会自动识别类型")


class ResponseModel(BaseModel):
    code: ResponseStatus = Field(title="本次修改请求的状态")
    message: ResponseStatusMessage = Field(title="请求结果")
    data: Any = Field(title="对应的数据")
