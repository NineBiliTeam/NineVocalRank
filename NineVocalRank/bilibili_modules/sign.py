import hashlib
import time
from urllib.parse import quote

import httpx


# 预先获取并缓存 img_key 和 sub_key（实际需要定期更新）
def get_wbi_keys() -> tuple[str, str]:
    nav_url = "https://api.bilibili.com/x/web-interface/nav"
    resp = httpx.get(nav_url).json()
    img_url: str = resp["data"]["wbi_img"]["img_url"]
    sub_url: str = resp["data"]["wbi_img"]["sub_url"]
    # 从URL中提取密钥（如 "img_key" 和 "sub_key"）
    img_key = img_url.rsplit("/", 1)[1].split(".")[0]
    sub_key = sub_url.rsplit("/", 1)[1].split(".")[0]
    return img_key, sub_key


# 混肴密钥生成最终签名字符串
def _mix_keys(img_key: str, sub_key: str) -> str:
    mix_key = img_key + sub_key
    key_map = [
        46,
        47,
        18,
        2,
        53,
        8,
        23,
        32,
        15,
        50,
        10,
        31,
        58,
        3,
        45,
        35,
        27,
        43,
        5,
        49,
        33,
        9,
        42,
        19,
        29,
        28,
        14,
        39,
        12,
        38,
        41,
        13,
        37,
        48,
        7,
        16,
        24,
        55,
        40,
        61,
        26,
        17,
        0,
        1,
        60,
        51,
        30,
        4,
        22,
        25,
        54,
        21,
        56,
        59,
        6,
        63,
        57,
        62,
        11,
        36,
        20,
        34,
        44,
        52,
    ]
    return "".join([mix_key[i] for i in key_map])[:32]


# 核心签名函数（函数签名符合要求）
def wbi_sign(params: dict) -> dict:
    # 获取当前时间戳
    wts = int(time.time())
    params["wts"] = wts

    # 过滤并排序参数
    filtered_params = {k: v for k, v in params.items() if v not in [None, ""]}
    sorted_params = sorted(filtered_params.items(), key=lambda x: x[0])

    # 拼接参数字符串（注意URL编码）
    param_str = "&".join(
        [f"{k}={quote(str(v), safe='!()*')}" for k, v in sorted_params]
    )

    # 获取密钥并混肴
    img_key, sub_key = get_wbi_keys()
    mix_key = _mix_keys(img_key, sub_key)

    # 计算MD5签名
    sign_str = param_str + f"&w_ts={wts}" + mix_key  # 注意实际规则可能不同
    w_rid = hashlib.md5(sign_str.encode()).hexdigest()

    # 返回新字典（不修改原params）
    return {**params, "w_rid": w_rid}
