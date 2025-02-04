# 测试用例
import pytest

from bilibili_modles.Video import Video
from filter.buildin_filters.NBVCDatabaseFilter import NBVCDatabaseFilter

videos = [
    # ------------正常数据部分--------------------
    # 中文VOCALOID
    ("BV1owCAYnEvF", True),
    ("BV1XykoYtE3P", True),
    ("BV1KNx3e8ETG", True),
    ("BV1s5xPegEPZ", True),
    ("av112977722344665", True),
    ("av113122694139335", True),
    ("AV113101974276078", True),
    ("AV113112577475673", True),
    ("AV1006464026", True),
    # -----------错误数据：非VC分区---------------
    ("BV1D7cZe6E2k", False),  # 科技区
    ("BV1ru411p7eD", False),  # 我不知道瞎找的
    ("BV1Lo4y1i7uU", False),
    ("BV1QmwNeAEx4", False),
    ("BV1ws411v7zE", False),
    ("BV1MA411M799", False),
    # -----------错误数据：过滤器的最！大！对！手！：日V--------------
    ("BV1sY4y1i7fB", False),
    ("BV19QfpYkEzk", False),
    ("BV1wbwze5EwH", False),
    ("BV1nafnYUEac", False),
    ("BV1Km4y1p7dd", False),
    ("BV1qDUPYKEzf", False),
    ("BV1GADYYmEnd", False),
    ("BV1Fs411a7mr", False),
    ("BV1194y197Re", False),
    ("BV1p4yDYYEZ7", False),
    # ----------------错误数据：不符合NBVC排除规则---------------
    ("BV1Xpr6YyErN", False),
    ("BV1qDUPYKEzf", False),
    ("BV1wYwTeHEEW", False),
]

filter_ = NBVCDatabaseFilter()


@pytest.mark.parametrize("bvid, result", videos)
async def test_vocaloid_china_filter(bvid, result):
    video = Video(bvid)
    await video.async_update_basic_data()
    f_result = await filter_.check(video)
    assert f_result == result
