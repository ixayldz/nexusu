"""Application logging utilities."""

import json
import logging
import sys


class _JsonFormatter(logging.Formatter):
    """A minimal JSON log formatter.

    Only the level and message are emitted which keeps dependencies light and
    avoids pulling in third party logging libraries such as *loguru*.
    """

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        payload = {"level": record.levelname, "message": record.getMessage()}
        return json.dumps(payload)


def setup_logging(level: str = "INFO") -> None:
    """Configure root logger to emit JSON to stdout.

    This mirrors the behaviour of the previous loguru-based implementation but
    relies solely on the standard library, making test environments lighter.
    """

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_JsonFormatter())

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level.upper())
