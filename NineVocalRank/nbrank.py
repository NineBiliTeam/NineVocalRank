import StartUp
from buildin_apis.basic.v1 import basic_v1_router
from filter.buildin_filters import VocaloidChinaFilter
from filters.test_vocaloid_china_filter import filter_
from http_utils.proxy.proxy_pools import MixinProxyPool, NoneProxyPool, JHaoProxyPool
from scheduler.reset_database import reset_database

"""
NineVocalRank
在这里编辑你的启动配置
这是个启动脚本示例
"""

# 在routers列表内写入你要启用的路由模块

if __name__ == "__main__":
    # 初始化NineBiliRank
    StartUp.init(
        tasks_=[
            [
                (reset_database, "cron"),
                {"day_of_week": "sat", "hour": 0},
            ]
        ],
        routers_=[basic_v1_router],
    )
    # 启动NineBiliRank
    StartUp.run()
