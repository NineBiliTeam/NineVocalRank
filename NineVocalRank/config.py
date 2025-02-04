import threading
from hashlib import md5
from pathlib import Path
from typing import Any

from filter.BaseFilter import BaseFilter
from http_utils.proxy.BaseProxyPool import BaseProxyPool
from logger import logger
from utils.config_utils import init_config

__NBR_VERSION__ = "0.0.1-beta"

buildin_proxy_pools = {}


def reg_buildin_proxy_pool(info: dict[str, type[BaseProxyPool]]):
    """注册内建代理源， 传入类名"""
    buildin_proxy_pools.update(info)


from http_utils.proxy import *

logger.debug(f"已经注册代理源：{buildin_proxy_pools}")

buildin_filters = dict()


def reg_buildin_filter(info: dict):
    """注册内建过滤器， 传入类名"""
    buildin_filters.update(info)


from filter.buildin_filters import *


logger.debug(f"已经注册过滤器：{buildin_filters}")


def get_config(*arg, **kwargs):
    return get_config_from_file()


def get_config_from_file():
    # 读取配置文件
    config = {"basic_config": init_config(Path("BasicConfig.yml"))}
    config.update(
        {
            "config": init_config(
                Path(f"config.{config["basic_config"]["config"]["config_env"]}.yml")
            )
        }
    )
    config["other_configs"] = dict()

    for key in config["basic_config"]["config"]["other_config_file"]:
        config["other_configs"].update(
            {
                key: init_config(
                    Path(config["basic_config"]["config"]["other_config_file"][key])
                )
            }
        )
    return config


def get_apikey():
    """获取API密钥"""
    raw = get_config()["basic_config"]["server"]["apikey"]
    if raw == "":
        return ""
    return md5(raw.encode()).hexdigest()


def get_proxy_pool():
    from http_utils.proxy.proxy_pools import NoneProxyPool

    if Config.has_instance():
        return Config.get_instance().proxy_pool
    return NoneProxyPool()


def get_filter():
    if Config.has_instance():
        return Config.get_instance().filter
    return NoneFilter()


class Config:
    _instance = None
    _lock1 = threading.Lock()
    _lock2 = threading.Lock()

    @classmethod
    def has_instance(cls):
        return cls._instance is not None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        with cls._lock1:
            if not cls._instance:
                with cls._lock2:
                    if not cls._instance:
                        cls._instance = cls(*args, **kwargs)
        return cls._instance

    def __init__(
        self,
        filter_: tuple[BaseFilter, tuple[Any], dict[Any]] = None,
        proxy_pool: tuple[BaseProxyPool, tuple[Any], dict[Any]] = None,
    ):
        """
        NBRank配置
        config为存储了全部配置的字典
        BasicConfig的配置会在`basic_config`字典中
        通用配置（config.<env>.yml）的配置会在`config`字典中
        第三方配置（XXX.yml）会在["other_configs"]字典中的XXX字典中（对应的文件名）
        :param filter_: (自定义过滤器, 位置参数列表, 名字参数字典)
        :param proxy_pool: (自定义的代理池, 位置参数列表, 名字参数字典)
        """
        if filter_ is None:
            filter_ = (buildin_filters["None"], tuple(), dict)
        if proxy_pool is None:
            from http_utils.proxy.proxy_pools.NoneProxyPool import NoneProxyPool

            proxy_pool = (NoneProxyPool, tuple(), dict())

        self._config = get_config_from_file()
        logger.info(f"载入配置：{self._config}")

        # 设置代理源
        if self._config["basic_config"]["spyder"]["proxy"] in buildin_proxy_pools:
            self._proxy_pool = buildin_proxy_pools[
                self._config["basic_config"]["spyder"]["proxy"]
            ]
            self._proxy_pool_args = (tuple, dict())
            logger.success(
                f"使用内建代理源：{self._config["basic_config"]["spyder"]["proxy"]}"
            )
        else:
            self._proxy_pool = proxy_pool[0]
            self._proxy_pool_args = (proxy_pool[1], proxy_pool[2])
            logger.success(f"使用自定义代理源：{proxy_pool[0]}")

        # 配置过滤器
        if self._config["basic_config"]["filter"]["type"] in buildin_filters:
            self._filter = buildin_filters[
                self._config["basic_config"]["filter"]["type"]
            ]
            self._filter_args = (tuple(), dict())
            logger.success(
                f"使用内置过滤器：{self._config["basic_config"]["filter"]["type"]}"
            )
        else:
            self._filter = filter_[0]
            self._filter_args = (filter_[1], filter_[2])
            logger.success(f"使用自定义过滤器：{filter_[0]()}")

    @property
    def proxy_pool(self):
        return self._proxy_pool(*self._proxy_pool_args[0], **self._proxy_pool_args[1])

    @property
    def config(self):
        return self._config

    @property
    def filter(self):
        return self._filter(*self._filter_args[0], **self._filter_args[1])
