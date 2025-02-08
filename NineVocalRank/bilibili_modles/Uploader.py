import time
import warnings

from pydantic import BaseModel, Field

from exceptions.BilibiliException import BilibiliRequestException
from http_utils.http import HttpRequest


class Uploader(BaseModel):
    mid: str = Field(title="UP主的mid", default="")
    name: str = Field(title="UP主的用户名", default="")
    fans: int = Field(title="UP主的粉丝数", default=0)
    archive_count: int = Field(title="UP主的稿件数量", default=0)
    timestamp: int = Field(title="数据更新时间戳", default=0)

    def __init__(
        self,
        mid: str,
        name: str = "",
        fans: int = 0,
        archive_count: int = 0,
        timestamp: int = int(time.time()),
    ):
        """
        UP主数据类
        **注意** 造完的UP主对象**默认不带**任何数据，需要调用`update_basic_data()`（同步）或者`async_update_basic_data`（异步）更新数据
        :param mid: UP主的mid
        """
        super().__init__()
        self.mid = mid
        self.name = name
        self.fans = fans
        self.archive_count = archive_count
        self._http = HttpRequest()
        self.timestamp = timestamp

    async def async_update_basic_data(self):
        async_session = await self._http.get_async_session()
        resp = await async_session.get(
            "https://api.bilibili.com/x/web-interface/card", params={"mid": self.mid}
        )
        resp = resp.json()
        self._set_new_data(resp)

    def update_basic_data(self):
        warnings.warn("此方法已废弃，不推荐使用", DeprecationWarning)
        resp = self._http.session.get(
            "https://api.bilibili.com/x/web-interface/card", params={"mid": self.mid}
        ).json()
        self._set_new_data(resp)

    def _set_new_data(self, data: dict):
        if data["code"] != 0:
            raise BilibiliRequestException(
                f"请求UP主{self.name}({self.mid})错误，响应：{data}"
            )
        data = data["data"]
        self.fans = data["card"]["fans"]
        self.name = data["card"]["name"]
        self.archive_count = data["archive_count"]
