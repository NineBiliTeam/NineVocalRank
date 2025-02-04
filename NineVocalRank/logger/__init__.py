import sys

from loguru import logger

logger.remove(0)
logger.add(
    sys.stdout,
    format="<level><u>{time:zz YYYY-MM-DD HH:mm:ss}</u> <b>[{level}]</b>[{name}|{module}|{line}]|-> {message}</level>",
    level=20,
)
