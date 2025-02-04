import pytest

from http_utils.proxy.Proxy import Proxy
from http_utils.proxy.proxy_pools.JHaoProxyPool import JHaoProxyPool

pools_to_test = [JHaoProxyPool()]


@pytest.mark.parametrize("pool", pools_to_test)
def test_proxy(pool):
    for _ in range(5):
        new_proxy = pool.get_proxy()
        # print(type(new_proxy))

        assert isinstance(new_proxy, Proxy)


@pytest.mark.parametrize("pool", pools_to_test)
async def test_async_proxy(pool):
    for _ in range(5):
        new_proxy = await pool.async_get_proxy()
        # print(type(new_proxy))
        assert isinstance(new_proxy, Proxy)
