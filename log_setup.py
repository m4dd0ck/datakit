"""Simple logging configuration."""

import logging
import sys
from pathlib import Path


def setup_logging(
    name: str = "app",
    level: int = logging.INFO,
    log_file: str | None = None,
    fmt: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> logging.Logger:
    """Configure and return a logger.

    Args:
        name: Logger name
        level: Logging level (default INFO)
        log_file: Optional file path to write logs
        fmt: Log message format

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Clear existing handlers
    logger.handlers.clear()

    formatter = logging.Formatter(fmt)

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler if specified
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get or create a logger with the given name."""
    return logging.getLogger(name)


class LogContext:
    """Context manager that logs entry and exit."""

    def __init__(self, logger: logging.Logger, message: str):
        self.logger = logger
        self.message = message

    def __enter__(self):
        self.logger.info(f"Starting: {self.message}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.error(f"Failed: {self.message} - {exc_val}")
        else:
            self.logger.info(f"Completed: {self.message}")
        return False
