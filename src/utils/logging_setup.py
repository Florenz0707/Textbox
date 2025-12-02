from __future__ import annotations

import logging
from logging import Logger

from ..config.paths import PROJECT_ROOT
from ..config.settings import LOG_LEVEL


def _to_level(name: str) -> int:
    try:
        return getattr(logging, name.upper())
    except Exception:
        return logging.INFO


def setup_logging() -> Logger:
    """Configure root logger to write to project_root/log.txt (overwrite on start) and console.
    Level is taken from settings.LOG_LEVEL (DEBUG/INFO/WARNING/ERROR/CRITICAL).
    Safe to call multiple times; only configures once.
    """
    logger = logging.getLogger()
    if logger.handlers:
        # update level if already configured
        level = _to_level(LOG_LEVEL)
        logger.setLevel(level)
        for h in logger.handlers:
            h.setLevel(level)
        return logger

    log_file = PROJECT_ROOT / "log.txt"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    level = _to_level(LOG_LEVEL)
    logger.setLevel(level)

    fmt = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    fh = logging.FileHandler(str(log_file), mode="w", encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(fmt)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("Logging initialized at level %s -> %s", LOG_LEVEL, log_file)
    return logger
