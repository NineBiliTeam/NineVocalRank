from bilibili_modles.Video import Video
from filter.BaseFilter import BaseFilter


class NoneFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def check(self, video: Video) -> bool:
        return True


from config import reg_buildin_filter

reg_buildin_filter({"None": NoneFilter})
