from sqlalchemy.dialects.postgresql.psycopg import logger

from bilibili_modles.Video import Video
from database.utils.add_video import add_video_to_db
from http_utils.http import HttpRequest

_http = HttpRequest()


async def get_data_from_evocalrank():
    """
    从[周刊](evocalrank.com)注册视频
    周刊对不起
    """
    result = (
        await (await _http.get_async_session()).get(
            "https://www.evocalrank.com/data/info/latest.json"
        )
    ).json()
    keywords = [
        "main_rank",
        "oth_pickup",
        "super_hit",
        "pick_up",
        "Vocaloid_pick_up",
        "history-1-year",
        "history-10-year",
        "ed",
        "op",
    ]
    for keyword in keywords:
        if keyword in result:
            for video in result[keyword]:
                logger.info(f"收录周刊#{result["ranknum"]}的{video["avid"]}")
                await add_video_to_db(Video(video["avid"]))
    logger.info("周刊收录完毕！")
