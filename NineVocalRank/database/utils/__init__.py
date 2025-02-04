from sqlalchemy import Select

from database import async_session


async def search_by_sql(sql: Select):
    async with async_session() as session:
        resp = await session.scalars(sql)
        resp = resp.all()
        return resp
