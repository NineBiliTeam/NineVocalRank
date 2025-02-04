import pytest

from http_utils.http import HttpRequest

urls = [
    "https://www.bilibili.com",
    "https://www.baidu.com",
    "https://www.bing.com",
    "https://www.w3cschool.cn",
    "https://www.hao123.com/",
    "https://www.zhihu.com/",
    "https://www.163.com/",
    "https://blog.csdn.net/",
    "https://www.cnblogs.com/",
]


@pytest.mark.parametrize("url", urls)
def test_http(url):
    session = HttpRequest()
    session.session.get(url)


@pytest.mark.parametrize("url", urls)
async def test_async_http(url):
    session = HttpRequest()
    session = await session.get_async_session()
    await session.get(url)
