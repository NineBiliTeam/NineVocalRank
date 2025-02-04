import time
import warnings

from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from exceptions.BilibiliException import (
    BilibiliPermissionException,
    BilibiliRequestException,
)
from http_utils.http import HttpRequest
from utils.bilibili_utils import is_avid, is_bvid

VideoInvisible = 62002
VideoReviewing = 62004
UploaderPrivateVideo = 62012
VideoNotExist = -404
LackOfPermissions = -403
RequestException = -400
Success = 0


class VideoStat(TypedDict):
    view: int
    like: int
    coin: int
    favorite: int
    reply: int
    share: int
    danmaku: int


class VideoInfo(TypedDict):
    uploader_mid: int
    uploader_name: str
    title: str
    pic: str
    pages: int
    timestamp: int


class VideoID(TypedDict):
    bvid: str
    avid: str
    tid: int


class Video(BaseModel):
    """
    B站视频类
    传入AV号/BV号即可构造
    """

    video_stat: VideoStat = Field(
        title="视频数据信息",
        default={
            "view": 0,
            "like": 0,
            "coin": 0,
            "favorite": 0,
            "reply": 0,
            "share": 0,
            "danmaku": 0,
        },
    )
    video_info: VideoInfo = Field(
        title="视频特征信息",
        default={
            "uploader_mid": 0,
            "uploader_name": "",
            "title": "",
            "pic": "",
            "pages": 0,
        },
    )
    video_id: VideoID = Field(title="视频ID信息", default={"avid": "", "bvid": ""})

    def __init__(
        self,
        video_id: str,
        view: int = 0,
        like: int = 0,
        coin: int = 0,
        favorite: int = 0,
        share: int = 0,
        reply: int = 0,
        danmaku: int = 0,
        avid: str = "",
        bvid: str = "",
        title: str = "",
        pic: str = "",
        pages: int = 0,
        uploader_mid: int = 0,
        tid: int = 0,
        timestamp: int = int(time.time()),
    ):
        super().__init__()
        """
        构造视频对象
        **注意** 构造完的视频对象**不带**任何数据，需要调用`update_basic_data()`（同步）或者`async_update_basic_data`（异步）更新数据
        :param video_id:AV号或者BV号1
        """
        if avid and bvid:
            self.video_id = VideoID(avid=avid, bvid=bvid, tid=tid)
        else:
            if is_avid(video_id):
                self.video_id = VideoID(avid=video_id, bvid="", tid=0)
            elif is_bvid(video_id):
                self.video_id = VideoID(avid="", bvid=video_id, tid=0)
            else:
                raise BilibiliRequestException(
                    f"输入的不是一个合法的视频ID！({video_id})"
                )
        self.video_stat = VideoStat(
            view=view,
            like=like,
            coin=coin,
            favorite=favorite,
            reply=reply,
            share=share,
            danmaku=danmaku,
        )
        self.video_info = VideoInfo(
            uploader_mid=uploader_mid,
            uploader_name=title,
            title=title,
            pic=pic,
            pages=pages,
            timestamp=timestamp,
        )
        self._http = HttpRequest().get_instance()
        self.video_id["avid"] = self.video_id["avid"].lower().replace("av", "")

    async def get_video_desc(self):
        resp = self._http.session.get(
            "https://api.bilibili.com/x/web-interface/wbi/view",
            params={"aid": self.video_id["avid"], "bvid": self.video_id["bvid"]},
        ).json()
        self._check_resp_stat(resp)
        return resp["data"]["desc"]

    async def get_video_tags(self):
        resp = self._http.session.get(
            "https://api.bilibili.com/x/tag/archive/tags",
            params={"aid": self.video_id["avid"], "bvid": self.video_id["bvid"]},
        ).json()
        self._check_resp_stat(resp)
        tags = list()
        for tag in resp["data"]:
            tags.append(tag["tag_name"])
        return tags

    async def async_update_basic_data(self):
        """异步更新视频数据"""

        resp = self._http.session.get(
            "https://api.bilibili.com/x/web-interface/wbi/view",
            params={"aid": self.video_id["avid"], "bvid": self.video_id["bvid"]},
        )
        self._set_new_stat(resp.json())

    def _set_new_stat(self, resp: dict):
        self._check_resp_stat(resp)
        data = resp["data"]
        self.video_id["bvid"] = data["bvid"]
        self.video_id["avid"] = str(data["aid"])
        self.video_id["tid"] = data["tid"]
        stat = data["stat"]
        self.video_stat["view"] = stat["view"]
        self.video_stat["like"] = stat["like"]
        self.video_stat["coin"] = stat["coin"]
        self.video_stat["favorite"] = stat["favorite"]
        self.video_stat["reply"] = stat["reply"]
        self.video_stat["share"] = stat["share"]
        self.video_stat["danmaku"] = stat["danmaku"]

        self.video_info["pages"] = len(data["pages"])
        self.video_info["title"] = data["title"]
        self.video_info["uploader_mid"] = data["owner"]["mid"]
        self.video_info["uploader_name"] = data["owner"]["name"]

        self.video_info["timestamp"] = int(time.time())

    def _check_resp_stat(self, resp):
        if resp["code"] == LackOfPermissions:
            raise BilibiliPermissionException(
                f"获取{self.video_id}失败，因为：权限不足。响应：{resp}"
            )
        elif resp["code"] == VideoReviewing:
            raise BilibiliPermissionException(
                f"获取{self.video_id}失败，因为：视频审核中。响应：{resp}"
            )
        elif resp["code"] == RequestException:
            raise BilibiliRequestException(
                f"获取{self.video_id}失败，因为：请求错误。响应：{resp}"
            )
        elif resp["code"] == VideoInvisible:
            raise BilibiliPermissionException(
                f"获取{self.video_id}失败，因为：视频不可见。响应：{resp}"
            )
        elif resp["code"] == UploaderPrivateVideo:
            raise BilibiliPermissionException(
                f"获取{self.video_id}失败，因为：视频仅UP主可见。响应：{resp}"
            )
        elif resp["code"] == VideoNotExist:
            raise BilibiliPermissionException(
                f"获取{self.video_id}失败，因为：视频不存在。响应：{resp}"
            )

    def update_basic_data(self):
        warnings.warn("此方法已废弃，不推荐使用", DeprecationWarning)
        """同步更新视频数据"""
        resp = self._http.session.get(
            "https://api.bilibili.com/x/web-interface/wbi/view",
            params={"aid": self.video_id["avid"], "bvid": self.video_id["bvid"]},
        )
        self._set_new_stat(resp.json())
