from fastapi import HTTPException, status
from fastapi.params import Header

from config import get_apikey

key = get_apikey()


async def key_auth(
    x_apikey: str = Header(
        title="在BasicConfig.yml里面设置的api密钥的md5散列", default=""
    )
):
    if key == "":
        return
    if x_apikey != key:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
