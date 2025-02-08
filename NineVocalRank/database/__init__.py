from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import get_config
from .Base import Base

config = get_config()

enable_async = config["basic_config"]["spyder"]["async"]["enable"]
task_count = config["basic_config"]["spyder"]["async"]["task_count"]
# sync_engine = create_engine(config["basic_config"]["database"]["db_url"])
if enable_async:
    async_engine = create_async_engine(config["basic_config"]["database"]["db_url"], pool_size=task_count , max_overflow=64)
else:
    async_engine = create_async_engine(config["basic_config"]["database"]["db_url"])

async_session = async_sessionmaker(async_engine)
# session = sessionmaker(sync_engine)

from .Base import Base
from .model.Uploader import UploaderDB
from .model.Video import VideoDB
