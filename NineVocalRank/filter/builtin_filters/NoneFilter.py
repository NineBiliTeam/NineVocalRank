from bilibili_modules.Video import Video
from filter.BaseFilter import BaseFilter


class NoneFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def check(self, video: Video) -> (bool, str):
        return True, ""


from config import reg_builtin_filter

reg_builtin_filter({"None": NoneFilter})
