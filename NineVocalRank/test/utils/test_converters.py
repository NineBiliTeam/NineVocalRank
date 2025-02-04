import pytest

from bilibili_modles.Uploader import Uploader
from bilibili_modles.Video import Video
from utils.to_models import video_model_to_db, uploader_model_to_db
from utils.to_schemas import video_db_to_model, uploader_db_to_model

videos = [
    # ------------正常数据部分--------------------
    # 中文VOCALOID
    "BV1owCAYnEvF",  # 正常的BV号,且是中文VOCALOID视频
    "BV1XykoYtE3P",  # 正常的BV号,且是中文VOCALOID视频
    "BV1KNx3e8ETG",  # 正常的BV号,且是中文VOCALOID视频
    "BV1s5xPegEPZ",  # 正常的BV号,且是中文VOCALOID视频
    "BV1p4yDYYEZ7",  # 正常的BV号,且是中文VOCALOID视频
    "av112977722344665",  # 正常的AV号,且是中文VOCALOID视频
    "av113122694139335",  # 正常的AV号,且是中文VOCALOID视频
    "AV113101974276078",  # 正常的AV号,且是中文VOCALOID视频，但是AV大写
    "AV113112577475673",  # 正常的AV号,且是中文VOCALOID视频，但是AV大写
    "AV1006464026",  # 正常的AV号,且是中文VOCALOID视频， 但是AV大写
]

uploaders = [
    # ----------正确数据----------
    3379951,  # 教主
    526573745,  # 点点
    112428,  # 校长
    673779175,  # 量子位
    352831167,  # 青空酱
    341368,  # 存娘
    1767947324,  # 可爱玛丽
    7980111,  # TOMMMMMMMMMMMMMMMMMMMMMMMM
    393416910,  # 神奇雷雷子
    84136150,  # 我是我到底是不是鱼丸君
    346563107,  # 我们cn自己的军情六处
    326499679,  # 哔哩哔哩南瓜
    3546755448703548,  # TEAM VCPIDEA
    1792710157,  # 凑热闹的
    354278618,  # 爱慕细外星人
]


@pytest.mark.parametrize("video", videos)
def test_video_converters(video):
    video_model = Video(video)
    video_model.update_basic_data()
    checker = video_model.model_copy()
    video_db = video_model_to_db(video_model)
    model2 = video_db_to_model(video_db)
    assert checker == model2


@pytest.mark.parametrize("uploader", uploaders)
def test_video_converters(uploader):
    uploader_model = Uploader(uploader)
    uploader_model.update_basic_data()
    checker = uploader_model.model_copy()
    uploader_db = uploader_model_to_db(uploader_model)
    model2 = uploader_db_to_model(uploader_db)
    assert checker == model2
