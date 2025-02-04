import httpx
from httpx import AsyncClient

from exceptions.nbr_exception import NBRLoadException
from http_utils.proxy.BaseProxyPool import BaseProxyPool
from http_utils.proxy.Proxy import Proxy


class JHaoProxyPool(BaseProxyPool):
    def __init__(self):
        super(JHaoProxyPool, self).__init__()
        try:
            from config import get_config

            config = get_config()
        except KeyError:
            raise NBRLoadException(
                "无法载入配置文件！请检查配置选项（JHaoProxyPool配置文件路径未载入）"
            )
        self._api_url = config["other_configs"]["JHaoProxyPool"]["api"]["url"]

    def get_proxy(self):
        try:
            resp = httpx.get(f"{self._api_url}/get/").json()
        except httpx.ReadTimeout:
            return Proxy()
        if not "proxy" in resp:
            return Proxy()
        return Proxy(resp["proxy"], is_https=resp["https"])

    async def async_get_proxy(self):
        session = AsyncClient()
        try:
            resp = await session.get(f"{self._api_url}/get/")
        except httpx.ReadTimeout:
            return Proxy()
        resp = resp.json()
        if not "proxy" in resp:
            return Proxy()

        return Proxy(resp["proxy"], is_https=resp["https"])


from config import reg_buildin_proxy_pool

reg_buildin_proxy_pool({"JHaoProxyPool": JHaoProxyPool})
