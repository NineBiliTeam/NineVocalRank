from bilibili_modles.Video import Video
from config import reg_buildin_filter
from filter.buildin_filters.VocaloidChinaFilter import VocaloidChinaFilter

uploader_blacklist = [
    # 屏蔽规则1.4: 拒绝收录的UP主
    1037289255
]

video_blacklist = [
    # 屏蔽规则2.2：被鉴定为买量的曲目
]


class NBVCDatabaseFilter(VocaloidChinaFilter):

    def __init__(self):
        """
        依赖于VocaloidChinaFilter的，更严格的过滤器
        遵照NBVCDatabase收录规则运行
        """
        super().__init__()

    async def check(self, video: Video) -> bool:
        # NBVC检查1：被排除排名的UP主
        for mid in uploader_blacklist:
            if video.video_info["uploader_mid"] == mid:
                return False

        # NBVC检查2：被鉴定为买量的曲目
        for vid in video_blacklist:
            if video.video_id["bvid"] == vid or video.video_id["avid"] == vid:
                return False
        # 调用父类的检查
        return await super().check(video)


reg_buildin_filter({"NBVCDatabaseFilter": NBVCDatabaseFilter})
