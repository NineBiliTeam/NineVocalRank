from http_utils.proxy.BaseProxyPool import BaseProxyPool
from http_utils.proxy.Proxy import Proxy


class MixinProxyPool(BaseProxyPool):

    def __init__(self, pools: list[BaseProxyPool.__class__]):
        """
        混合代理池.
        可以启用多个代理池，在其中找到一个可用代理.
        需要传入代理源实例列表.
        :param pools:
        """
        super().__init__()
        self.pools = pools

    def get_proxy(self) -> Proxy:
        for pool in self.pools:
            proxy = pool().get_proxy()
            if proxy.ip is not None:
                return proxy
        return Proxy()

    async def async_get_proxy(self) -> Proxy:
        for pool in self.pools:
            proxy = await pool.async_get_proxy()
            if proxy.ip is not None:
                return proxy
        return Proxy()
