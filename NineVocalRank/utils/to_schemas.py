from bilibili_modles.Uploader import Uploader
from bilibili_modles.Video import Video
from database.model.Uploader import UploaderDB
from database.model.Video import VideoDB


def uploader_db_to_model(db_uploader: UploaderDB) -> Uploader:
    return Uploader(
        mid=db_uploader.mid,
        name=db_uploader.name,
        fans=db_uploader.fans,
        archive_count=db_uploader.archive_count,
        timestamp=db_uploader.timestamp,
    )


def video_db_to_model(db_video: VideoDB) -> Video:
    return Video(
        video_id="",
        bvid=db_video.bvid,
        avid=db_video.avid,
        timestamp=db_video.timestamp,
        title=db_video.title,
        uploader_mid=db_video.uploader_mid,
        like=db_video.like,
        coin=db_video.coin,
        favorite=db_video.favorite,
        view=db_video.view,
        reply=db_video.reply,
        share=db_video.share,
        danmaku=db_video.danmaku,
        pic=db_video.pic,
        pages=db_video.pages,
    )
