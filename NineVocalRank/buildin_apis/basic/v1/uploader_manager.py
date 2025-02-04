from fastapi import APIRouter, Depends, Form

from bilibili_modles.Uploader import Uploader
from buildin_apis.basic.v1.models import (
    ResponseModel,
    ResponseStatusMessage,
    ResponseStatus,
)
from buildin_apis.depends.key_auth import key_auth
from database.utils.add_uploader import add_uploader_to_db
from database.utils.delete_uploader import delete_uploader
from database.utils.update_uploader import update_uploader

uploader_manager_router = APIRouter(
    prefix="/UploaderManager", tags=["Manage"], dependencies=[Depends(key_auth)]
)


@uploader_manager_router.post("/RegUploader")
async def reg_uploader(mid: int = Form(title="UP主的mid")) -> ResponseModel:
    uploader = Uploader(mid)
    await uploader.async_update_basic_data()

    await add_uploader_to_db(uploader)
    return ResponseModel(
        message=ResponseStatusMessage.success,
        code=ResponseStatus.success,
        data=uploader,
    )


@uploader_manager_router.post("/DeleteUploader")
async def delete_uploader_(mid: int = Form(title="UP主的mid")) -> ResponseModel:
    uploader = Uploader(mid)
    await uploader.async_update_basic_data()

    await delete_uploader(uploader)
    return ResponseModel(
        message=ResponseStatusMessage.success,
        code=ResponseStatus.success,
        data=uploader,
    )


@uploader_manager_router.post("/UpdateUploader")
async def update_uploader_(mid: int = Form()) -> ResponseModel:
    uploader = Uploader(mid)
    await uploader.async_update_basic_data()
    await update_uploader(uploader)
    return ResponseModel(
        message=ResponseStatusMessage.success,
        code=ResponseStatus.success,
        data=uploader,
    )
