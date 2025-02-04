from sqlalchemy import select

from bilibili_modles.Uploader import Uploader
from database.model.Uploader import UploaderDB
from database.utils import search_by_sql
from utils.to_schemas import uploader_db_to_model


def make_uploader_model_list_from_db_list(raw: list[UploaderDB] | UploaderDB):
    return [uploader_db_to_model(uploader) for uploader in raw]


async def search_uploader_by_mid(mid) -> list[Uploader]:
    sql = select(UploaderDB).where(UploaderDB.mid == mid)
    result = await search_by_sql(sql)
    return make_uploader_model_list_from_db_list(result)


async def search_uploader_by_name_keyword(name) -> list[Uploader]:
    sql = select(UploaderDB).where(UploaderDB.name.like(f"%{name}%"))
    result = await search_by_sql(sql)
    return make_uploader_model_list_from_db_list(result)
