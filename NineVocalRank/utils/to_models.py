import time

from bilibili_modles.Uploader import Uploader
from bilibili_modles.Video import Video
from database.model.Uploader import UploaderDB
from database.model.Video import VideoDB


def uploader_model_to_db(uploader: Uploader) -> UploaderDB:
    return UploaderDB(
        mid=uploader.mid,
        name=uploader.name,
        fans=uploader.fans,
        archive_count=uploader.archive_count,
        timestamp=int(time.time()),
    )


def video_model_to_db(video: Video) -> VideoDB:
    return VideoDB(
        view=video.video_stat["view"],
        like=video.video_stat["like"],
        coin=video.video_stat["coin"],
        favorite=video.video_stat["favorite"],
        reply=video.video_stat["reply"],
        share=video.video_stat["share"],
        danmaku=video.video_stat["danmaku"],
        timestamp=int(time.time()),
        uploader_mid=video.video_info["uploader_mid"],
        title=video.video_info["title"],
        pic=video.video_info["pic"],
        pages=video.video_info["pages"],
        avid=video.video_id["avid"],
        bvid=video.video_id["bvid"],
        tid=video.video_id["tid"],
    )
