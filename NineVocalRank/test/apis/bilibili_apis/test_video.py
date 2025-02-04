import pytest

from bilibili_modles.Video import Video
from exceptions.BilibiliException import BilibiliVideoException, BilibiliException

# 测试用例
videos = [
    # ------------正常数据部分--------------------
    # 中文VOCALOID
    ("BV1owCAYnEvF", "bvid"),  # 正常的BV号,且是中文VOCALOID视频
    ("BV1XykoYtE3P", "bvid"),  # 正常的BV号,且是中文VOCALOID视频
    ("BV1KNx3e8ETG", "bvid"),  # 正常的BV号,且是中文VOCALOID视频
    ("BV1s5xPegEPZ", "bvid"),  # 正常的BV号,且是中文VOCALOID视频
    ("BV1p4yDYYEZ7", "bvid"),  # 正常的BV号,且是中文VOCALOID视频
    ("av112977722344665", "avid"),  # 正常的AV号,且是中文VOCALOID视频
    ("av113122694139335", "avid"),  # 正常的AV号,且是中文VOCALOID视频
    ("AV113101974276078", "avid"),  # 正常的AV号,且是中文VOCALOID视频，但是AV大写
    ("AV113112577475673", "avid"),  # 正常的AV号,且是中文VOCALOID视频，但是AV大写
    ("AV1006464026", "avid"),  # 正常的AV号,且是中文VOCALOID视频， 但是AV大写
    # -----------错误数据边界条件---------------
    ("这是乱写的，但是包含中文", "bvid"),  # 包含异常字符串
    ("ewFNKVDSLVKOPSdckv", "bvid"),  # 包含乱写的字符串
    ("av1234567890Au", "avid"),  # 边界条件：异常的AV号，结尾有异常字符串
    ("av1234567890qwdh", "avid"),  # 边界条件：异常的AV号，结尾有异常字符串
    ("av12345678qwd90", "avid"),  # 边界条件：异常的AV号，中间有异常字符串
    ("av123dw45wdq67890", "avid"),  # 边界条件：异常的AV号，中间有异常字符串
    ("BV1p4yDYavZ7", "bvid"),  # 边界条件：并不存在的BV号，其中有av字串
    ("BV1AVyDYYEZ7", "bvid"),  # 边界条件：并不存在的BV号，其中有AV字串
    ("BV1p4yDYYaV7", "bvid"),  # 边界条件：并不存在的BV号，其中有Av字串
    ("BV1p4yDYYEAv", "bvid"),  # 边界条件：并不存在的BV号，其中有aV字串
    (
        "BV1p你说你不想在这里4yDYavZ7",
        "bvid",
    ),  # 边界条件：错误的BV号，里面有不应该存在的字串
    (
        "BV1AVyDY我也不想在这里YEZ7",
        "bvid",
    ),  # 边界条件：并不存在的BV号，里面有不应该存在的字串
    (
        "BV1AVyDY但天黑得太快想走早就来不及YEZ7",
        "bvid",
    ),  # 边界条件：并不存在的BV号，里面有不应该存在的字串
    ("BV1p4yDY#$%^&*(YaV7", "bvid"),  # 边界条件：并不存在的BV号，里面有不应该存在的字串
    ("BV1p4&yDYYEAv", "bvid"),  # 边界条件：并不存在的BV号，里面有不应该存在的字串
]


@pytest.mark.run(order=1)
@pytest.mark.parametrize("video_id, video_id_type", videos)
def test_make_video(video_id, video_id_type):
    try:
        video = Video(video_id)
    except Exception as e:
        assert isinstance(e, (BilibiliVideoException, ValueError))
        return
    if video_id_type == "avid":
        assert isinstance(video.video_id["avid"], str)
    elif video_id_type == "bvid":
        assert isinstance(video.video_id["bvid"], str)


@pytest.mark.run(order=3)
@pytest.mark.parametrize("video_id, video_id_type", videos)
async def test_video_update_async(video_id, video_id_type):
    try:
        video = Video(video_id)
    except ValueError as e:
        assert True
        return
    try:
        await video.async_update_basic_data()
    except Exception as e:
        assert isinstance(e, BilibiliException)
        return
    assert video.video_stat["reply"] != 0
    assert video.video_stat["coin"] != 0
    assert video.video_stat["like"] != 0
    assert video.video_stat["view"] != 0
    assert video.video_stat["share"] != 0
    assert video.video_stat["favorite"] != 0
    assert video.video_stat["danmaku"] != 0
