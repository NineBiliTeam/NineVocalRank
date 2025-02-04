import abc

from http_utils.proxy.Proxy import Proxy


class BaseProxyPool:
    """
    爬虫代理池基类
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_proxy(self) -> Proxy:
        """
        获取随机代理的同步方法.
        如果无法实现则返回空代理
        :return: 随机代理
        """
        return None

    @abc.abstractmethod
    async def async_get_proxy(self) -> Proxy:
        """
        获取随机代理的异步方法
        如果无法实现则返回空代理
        :return: 随机代理
        """
        pass
