import httpx
import pytest

from bilibili_modles.Uploader import Uploader
from exceptions.BilibiliException import BilibiliRequestException

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


@pytest.mark.parametrize("mid", uploaders)
async def test_async_uploader(mid):
    uploader = Uploader(mid)
    try:
        await uploader.async_update_basic_data()
    except httpx.ConnectTimeout:
        return
    except Exception as e:
        assert type(e) == BilibiliRequestException
        return
    assert uploader.mid == mid
    assert uploader.fans != 0
    assert uploader.name != ""
    assert uploader.archive_count != 0
