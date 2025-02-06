from nine_vocal_rank.models.enums import VideoRank
from utils.math_utils import calculate_percentage


def get_basic_view(raw_view: float) -> float:
    """
    获取播放基础得点
    :param raw_view:原始播放数量
    :return:基本播放得点
    """
    if raw_view > 1_0000:
        return raw_view * 0.5 + 5000
    return raw_view


def get_like_points(raw_like: float, raw_coin: float) -> float:
    """
    获取基础点赞得点
    :param raw_like: 原始点单
    :param raw_coin: 原始投币
    :return: 基础点赞得点
    """
    if raw_like > raw_coin * 2:
        return raw_coin * 2
    return raw_like


def get_correct_a(
    basic_view: float, raw_favourite: float, raw_danmu: float, raw_reply: float
) -> float:
    """
    获取修正A
    :param basic_view:基础播放得点
    :param raw_favourite: 原始收藏
    :param raw_danmu: 原始弹幕
    :param raw_reply: 原始回复
    :return:修正A
    """
    return round(
        (
            (basic_view + raw_favourite)
            / (basic_view + raw_favourite + (raw_danmu + raw_reply) * 20)
        )
        ** 2,
        2,
    )


def get_correct_b(raw_coin: float, raw_favourite: float, raw_view: float) -> float:
    """
    获取修正B
    :param raw_coin:
    :param raw_favourite:
    :param raw_view:
    :return:修正B
    """
    if raw_favourite > raw_coin * 2:
        result = ((raw_coin**2) / (raw_view * raw_coin)) * 250
    else:
        result = (raw_favourite / raw_view) * 250
    result = round(result, 2)
    if result > 50:
        return 50
    return result


def get_correct_c(raw_coin: float, raw_favourite: float, raw_view: float) -> float:
    """
    获取修正C
    :param raw_coin:原始投币
    :param raw_favourite: 原始收藏
    :param raw_view: 原始播放
    :return: 修正C
    """
    if raw_coin > raw_favourite:
        result = ((raw_favourite / raw_coin**2) / (raw_view * raw_coin)) * 250
    else:
        result = (raw_coin / raw_view) * 250
    result = round(result, 2)
    if result > 50:
        return 50
    return result


def get_correct_d(raw_favourite: float, raw_coin: float, raw_view: float) -> float:
    """
    获取修正D
    :param raw_favourite: 原始收藏
    :param raw_coin: 原始投币
    :param raw_view: 原始播放
    :return:
    """
    if raw_favourite > raw_coin:
        result = (raw_coin / raw_view) * 25
    else:
        result = (raw_favourite / raw_view) * 25
    result = round(result, 2)
    if result > 1:
        return 1
    return result


def get_interactive_points(
    raw_reply: float, raw_danmu: float, correct_a: float
) -> float:
    """
    获取互动得点
    :param raw_reply: 原始回复
    :param raw_danmu: 原始弹幕
    :param correct_a: 修正A
    :return: 互动得点
    """
    return (raw_reply + raw_danmu) * correct_a * 15


def get_favourite_points(raw_favourite: float, correct_b: float) -> float:
    """
    获取收藏得点
    :param raw_favourite:
    :param correct_b:
    :return: 点赞得点
    """
    return raw_favourite * correct_b


def get_coin_point(raw_coin: float, correct_c) -> float:
    """
    获取投币得点
    :param raw_coin:原始投币
    :param correct_c: 修正C
    :return: 最终投币得点
    """
    return correct_c * raw_coin


def get_view_point(basic_view: float, correct_d: float) -> float:
    """
    获取播放得点
    :param basic_view:基础播放得点
    :param correct_d: 修正D
    :return:
    """
    return basic_view * correct_d


def get_final_score(
    raw_view: float,
    raw_like: float,
    raw_coin: float,
    raw_favourite: float,
    raw_reply: float,
    raw_danmu: float,
) -> float:
    """
    周刊在2025-1-11更新的周刊公式
    :param raw_view:原始播放增长量
    :param raw_like: 原始点赞增长量
    :param raw_coin: 原始投币增长量
    :param raw_favourite: 原始收藏增长量
    :param raw_reply: 原始回复增长量
    :param raw_danmu: 原始弹幕增长量
    :return: 最终周刊得分量
    """
    # 基础播放
    try:
        basic_view = get_basic_view(raw_view)
        # 四大天王
        correct_a = get_correct_a(basic_view, raw_favourite, raw_danmu, raw_reply)
        correct_b = get_correct_b(raw_coin, raw_favourite, raw_view)
        correct_c = get_correct_c(raw_coin, raw_favourite, raw_view)
        correct_d = get_correct_d(raw_favourite, raw_coin, raw_view)
        # 各种得点
        like_point = get_like_points(raw_like, raw_coin)
        view_point = get_view_point(basic_view, correct_d)
        favourite_point = get_favourite_points(raw_favourite, correct_b)
        coin_point = get_coin_point(raw_coin, correct_c)
        interactive_points = get_interactive_points(raw_reply, raw_danmu, correct_a)
        # 最终得分
        return (
            like_point + view_point + favourite_point + coin_point + interactive_points
        )
    except ZeroDivisionError:
        return 0


def get_rank(view) -> tuple[int, str, float]:
    """
    获取视频的VOCALOID成就
    :param view: 视频播放了
    :return: 成就代码，完成度
    """
    from nine_vocal_rank.models.VocaloidVideo import VideoRankCode

    if view < 10_0000:
        return (
            VideoRankCode.no_rank_song,
            VideoRank.no_rank_song,
            calculate_percentage(view, 10_0000),
        )
    if 10_0000 <= view < 100_0000:
        return (
            VideoRankCode.hall_of_fame_song,
            VideoRank.hall_of_fame_song,
            calculate_percentage(view, 100_0000),
        )
    if 100_0000 <= view < 1000_0000:
        return (
            VideoRankCode.legendary_song,
            VideoRank.legendary_song,
            calculate_percentage(view, 1000_0000),
        )
    else:
        return (
            VideoRankCode.mythical_song,
            VideoRank.mythical_song,
            calculate_percentage(view, view),
        )

def get_target_view(view:int):
    rank_code, _, _ = get_rank(view)
    target_view = 10 ** rank_code.value
    return target_view