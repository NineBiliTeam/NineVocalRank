import abc

from bilibili_modles.Video import Video


class BaseFilter:
    """
    视频过滤器基类
    用于过滤B站视频，留下符合收录规则视频进入数据库
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    async def check(self, video: Video) -> bool:
        """
        视频合法性检查器
        :param video:  B站视频对象
        :return: 视频是否合法。如果视频可被收录，返回True
        """
        pass
