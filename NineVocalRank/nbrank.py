import startup
from buildin_apis.basic.v1 import basic_v1_router
from buildin_hooks.reg_video_from_file import reg_video_from_file
from nine_vocal_rank.nvr_apis import nine_vocal_rank_router
from nine_vocal_rank.scheduler.achievement_monitor import achievement_monitor
from nine_vocal_rank.scheduler.get_data_from_evocalrank import get_data_from_evocalrank
from nine_vocal_rank.scheduler.get_sorted_database import get_sorted_database
from scheduler.reset_database import reset_database

"""
NineBiliRank
在这里编辑你的启动配置
这是个启动脚本示例
"""

# 在routers列表内写入你要启用的路由模块

if __name__ == "__main__":
    # 初始化NineBiliRank
    startup.init(
        tasks_=[
            [(reset_database, "cron"),{"day_of_week": "sat", "hour": 0},],
            [(get_data_from_evocalrank, "cron"),{"day_of_week": "sat", "hour": 0},],
            [(get_sorted_database, "cron"),{"hour": 0}],
            [(achievement_monitor, "interval"),{"hours": 6, "args":(5, )}],
            [(achievement_monitor, "interval"),{"hours": 3, "args":(4, )}],
            [(achievement_monitor, "interval"),{"hours": 1, "args":(3, )}],
            [(achievement_monitor, "interval"),{"minutes": 10, "args":(2, )}],
            [(achievement_monitor, "interval"),{"minutes": 1, "args":(1, )}],
        ],
        routers_=[basic_v1_router, nine_vocal_rank_router],
        start_hooks_=[],
        async_start_tasks_=[reg_video_from_file, get_sorted_database, get_data_from_evocalrank],
    )
    # 启动NineBiliRank
    startup.run()
