from pydantic import BaseModel, Field


class APIPluginMeta(BaseModel):
    name: str = Field(title="本模块的名称")
    description: str = Field(title="本模块的简介")
    author: str = Field(title="本模块的作者")
    version: str = Field(title="本模块的版本")
    plugin_type: str = Field(title="本模块的类型(buildin, data, rank)")
