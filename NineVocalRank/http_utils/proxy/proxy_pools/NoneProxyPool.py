from config import reg_buildin_proxy_pool
from http_utils.proxy.BaseProxyPool import BaseProxyPool
from http_utils.proxy.Proxy import Proxy


class NoneProxyPool(BaseProxyPool):

    def get_proxy(self) -> Proxy:
        return Proxy()

    def __init__(self):
        """
        空爬虫代理池，用于不使用代理时
        无论如何这货都会返回空代理
        """
        super().__init__()
        pass

    async def async_get_proxy(self) -> Proxy:
        return Proxy()


reg_buildin_proxy_pool({"None": NoneProxyPool})
