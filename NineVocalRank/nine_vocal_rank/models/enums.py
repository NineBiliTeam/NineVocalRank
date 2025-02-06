from enum import Enum


class VideoRank(Enum):
    no_rank_song: str = "无"
    hall_of_fame_song: str = "殿堂曲"  # 10万播放量级作品
    legendary_song: str = "传说曲"  # 百万播放量级作品
    mythical_song: str = "神话曲"  # 千万播放量级作品


class VideoRankCode(Enum):
    no_rank_song: int = 5
    hall_of_fame_song: int = 6  # 10万播放量级作品
    legendary_song: int = 7  # 百万播放量级作品
    mythical_song: int = 8  # 千万播放量级作品
