import sys

from loguru import logger


def setup_logging(level: str = "INFO") -> None:
    """
    JSON formatında stdout'a (Docker-friendly) log basar.
    """
    logger.remove()
    logger.add(
        sys.stdout,
        level=level.upper(),
        serialize=True,
        backtrace=False,
        diagnose=False,
    )
