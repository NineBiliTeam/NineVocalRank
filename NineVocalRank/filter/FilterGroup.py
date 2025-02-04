from filter.BaseFilter import BaseFilter


class FilterGroup(BaseFilter):
    def __init__(self, *filters: BaseFilter):
        """
        过滤器组
        由过滤器组成
        如果过滤器组内全部监测通过则此过滤器检测通过
        :param filters:过滤器
        """
        super().__init__()
        self.filters = filters

    def check(self, bvid: str = None, avid: str = None) -> bool:
        self._has_bv_or_av(bvid, avid)
        for filter_ in self.filters:
            if not filter_.check(bvid, avid):
                return False
        return True
