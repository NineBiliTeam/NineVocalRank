from bilibili_modles.Video import Video
from config import reg_buildin_filter
from filter.BaseFilter import BaseFilter

keywords = [
    # VSinger相关
    "洛天依",
    "言和",
    "乐正绫",
    "乐正龙牙",
    "徵羽摩柯",
    "墨清弦",
    "vsinger",
    "vocaloid china",
    "Vsinger创作激励计划",
    # 五维介质相关
    "平行四界",
    "五维介质",
    "星尘",
    "诗岸",
    "海伊",
    "苍穹",
    "赤羽",
    "永夜",
    "Minus",
    "牧心",
    "五维创作赛",
    # 引擎相关
    # 不添加Vocaloid和SV的原因：这两个可以广泛的用于日V创作，为了防止误判，所以不加
    "ace studio",
    "x studio",
    # 初音未来
    # 初音未来单开一列，这玩意最难判断，感谢你，米库撒嘛
    # 以后遇到漏的tag再补
    "初音未来v4c"
    # 中V相关
    "中文vocaloid",
    "vocaloid中文曲",
]

blacklist_keyword = [
    # 我是日本人
    "日文",
    "日语",
    # 我不是B站
    "nicovideo",
    "youtube",
    "drive.google.com",
    "twitter",
    "x.com",
]


class VocaloidChinaFilter(BaseFilter):

    def __init__(self):
        """
        中文虚拟歌手曲目过滤器
        本过滤器的收录规则遵循[周刊虚拟歌手排行榜](https://evocalrank.com)的收录规则
        部分规则可能无法实现，只实现基本识别
        """
        super().__init__()

    async def check(self, video: Video):
        # 投稿在Vocaloid·UTAU分区的歌曲
        if video.video_id["tid"] != 30:
            return False
        desc = (await video.get_video_desc()).lower()
        tags = await video.get_video_tags()
        title = video.video_info["title"].lower()
        # 黑名单：
        # 匹配标题，简介是否含有日V相关关键词
        for item in (title, desc):
            for keyword in blacklist_keyword:
                if keyword in item:
                    return False

        # 匹配tags中是否有关键词
        for tag in tags:
            for keyword in blacklist_keyword:
                if keyword in tag.lower():
                    return False

        # 匹配标题，简介是否含有中V特征关键词
        for item in (title, desc):
            for keyword in keywords:
                if keyword in item:
                    return True

        # 匹配tags中是否有关键词
        for tag in tags:
            for keyword in keywords:
                if keyword in tag.lower():
                    return True
        # 还没匹配到就算不行
        return False


reg_buildin_filter({"VocaloidChinaFilter": VocaloidChinaFilter})
