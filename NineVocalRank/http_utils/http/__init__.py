import random
import threading

import httpx
from fake_headers import Headers

from logger import logger


class HttpRequest:
    _instance = None
    _lock1 = threading.Lock()
    _lock2 = threading.Lock()

    def __init__(self):
        self._async_session = httpx.AsyncClient()
        self._session = httpx.Client()
        from config import get_proxy_pool

        self._proxy_pool = get_proxy_pool()
        pass

    @classmethod
    def get_instance(cls):
        with cls._lock1:
            if not cls._instance:
                with cls._lock2:
                    if not cls._instance:
                        cls._instance = HttpRequest()
            return cls._instance

    @staticmethod
    def _get_random_referer():
        from http_utils.http.referers import bilibili_referer_urls

        return random.choice(bilibili_referer_urls)

    @property
    def session(self):
        res = Headers().generate()
        res.update({"Referer": self._get_random_referer()})
        self._session.headers = res
        proxy = self._proxy_pool.get_proxy()
        self._session.proxies = proxy.json()
        logger.debug(f"本次使用代理：{self._session.proxies}")
        return self._session

    async def get_async_session(self):
        res = Headers().generate()
        res.update({"Referer": self._get_random_referer()})
        self._async_session.headers = res
        proxy = await self._proxy_pool.async_get_proxy()
        self._async_session.proxies = proxy.json()
        logger.debug(f"本次使用代理：{self._async_session.proxies}")
        return self._async_session
