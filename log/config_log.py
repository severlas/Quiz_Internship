from loguru import logger

logger.add(
    "logging/debug.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="10 MB",
    compression="zip",
)
