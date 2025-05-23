"""
Logging utilities for Python applications.

This module provides a simple interface for setting up and using logging
with both console and file handlers, with JSON formatting for structured logging.
"""

import json
import logging
import logging.handlers
from pathlib import Path
from typing import Any, Literal


class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs JSON strings."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as a JSON string."""
        log_record: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # Add any extra fields
        if hasattr(record, "extra") and record.extra:
            log_record.update(record.extra)

        return json.dumps(log_record, ensure_ascii=False)


def get_logger(
    name: str | None = None,
    *,
    log_level: int | str = logging.INFO,
    log_file: str | Path | None = None,
    log_format: Literal["json", "text"] = "text",
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Get or create a logger with the specified configuration.

    If called with just a name or no arguments, returns an existing logger
    or creates one with default settings. If configuration parameters are
    provided and the logger is new, it will be configured accordingly.

    Args:
        name: Name of the logger. If None, uses the root logger.
        log_level: Logging level (e.g., 'DEBUG', 'INFO')
        log_file: Path to the log file. If None, logs only to console
        log_format: Format of the logs - 'json' for structured JSON logs, 'text' for human-readable format
        max_bytes: Maximum size in bytes for a single log file before it gets rotated (default: 10MB)
        backup_count: Number of backup log files to keep when rotating (default: 5)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name if name is not None else "")

    # If logger already has handlers, assume it's configured and return it
    if logger.handlers:
        return logger

    # Set log level
    logger.setLevel(log_level)

    # Create formatter
    if log_format.lower() == "json":
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    # Console handler (always added)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if log file is specified
    if log_file:
        log_file = Path(log_file)
        # If path is relative, make it relative to project root (one level up from utils/)
        if not log_file.is_absolute():
            project_root = Path(__file__).parent.parent
            log_file = project_root / log_file
        # Create directory if it doesn't exist
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            str(log_file),  # Convert Path to string for compatibility
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


# Default logger instance
root_logger = get_logger()
