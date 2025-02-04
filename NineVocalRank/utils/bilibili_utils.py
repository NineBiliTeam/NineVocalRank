def is_avid(video_id: str) -> bool:
    """
    检查一个字符串是不是AV号
    :param video_id: 视频ID字符串
    :return: 是否为AVID
    """
    video_id = video_id.lower()
    try:
        int(video_id)
        return True
    except ValueError:
        pass
    if "av" in video_id:
        video_id = video_id.replace("av", "")
        try:
            int(video_id)
        except ValueError:
            return False
        return True
    return False


def is_bvid(video_id: str) -> bool:
    """
    检查一个字符串是不是BV号
    :param video_id: 视频ID字符串
    :return: 是否为BVID
    """
    video_id = video_id.lower()
    if "bv" in video_id:
        for s in video_id:
            if not "a" <= s <= "z" and not "0" <= s <= "9":
                return False
        return True
    return False
