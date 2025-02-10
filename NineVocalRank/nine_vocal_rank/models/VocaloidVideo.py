import time

from typing import TypedDict

from loguru import logger
from pydantic import Field

from bilibili_modles.Video import Video
from config import get_filter
from database.utils.add_video import add_video_to_db
from database.utils.search_video import search_video_by_bvid
from nine_vocal_rank.exceptions.database import VideoValidationError
from nine_vocal_rank.models.enums import VideoRank, VideoRankCode
from nine_vocal_rank.utils.vrank_score import get_final_score, get_rank


class VrankInfo(TypedDict):
    vrank_score: float
    rank: VideoRank
    rank_code: VideoRankCode
    progress_percentage: float


class VideoIncrease(TypedDict):
    view: int
    like: int
    coin: int
    favorite: int
    reply: int
    share: int
    danmaku: int


class VocaloidVideo(Video):
    video_increase: VideoIncrease = Field(
        title="视频数据增量",
        default={
            "view": 0,
            "like": 0,
            "coin": 0,
            "favorite": 0,
            "reply": 0,
            "share": 0,
            "danmaku": 0,
        },
    )
    vrank_info: VrankInfo = Field(
        title="视频成就信息",
        default={
            "vrank_score": 0,
            "rank": VideoRank.no_rank_song,
            "rank_code": VideoRankCode.no_rank_song,
            "progress_percentage": 0,
        },
    )

    def __init__(self, vid:str):
        """
        Vocaloid视频对象.
        提供周刊算分等其他功能
        传入Vid
        """
        super().__init__(vid)

    async def _async_get_vocalrank_score(self):
        video_dbs = await search_video_by_bvid(self.video_id["bvid"])
        if len(video_dbs) == 0:
            filter_ = get_filter()
            flag, reason = await filter_.check(self)
            if flag:
                await add_video_to_db(self)
                self.video_increase = {
                    "view": 0,
                    "like": 0,
                    "coin": 0,
                    "favorite": 0,
                    "reply": 0,
                    "share": 0,
                    "danmaku": 0,
                }
            else:
                raise VideoValidationError(f"视频不符合NBVCDatabase注册规则！原因：{reason}")
        else:
            video_db = video_dbs[0]
            self.video_increase = {
                "view": self.video_stat["view"] - video_db.video_stat["view"],
                "like": self.video_stat["like"] - video_db.video_stat["like"],
                "coin": self.video_stat["coin"] - video_db.video_stat["coin"],
                "favorite": self.video_stat["favorite"]
                - video_db.video_stat["favorite"],
                "reply": self.video_stat["reply"] - video_db.video_stat["reply"],
                "share": self.video_stat["share"] - video_db.video_stat["share"],
                "danmaku": self.video_stat["danmaku"] - video_db.video_stat["danmaku"],
            }
        return get_final_score(
            raw_view=self.video_increase["view"],
            raw_like=self.video_increase["like"],
            raw_coin=self.video_increase["coin"],
            raw_danmu=self.video_increase["danmaku"],
            raw_reply=self.video_increase["reply"],
            raw_favourite=self.video_increase["favorite"],
        )

    async def async_update_basic_data(self):
        await super().async_update_basic_data()
        score = await self._async_get_vocalrank_score()
        code, rank, progress_percentage = get_rank(self.video_stat["view"])
        self.vrank_info = {
            "vrank_score": score,
            "rank": rank,
            "rank_code": code,
            "progress_percentage": progress_percentage,
        }
