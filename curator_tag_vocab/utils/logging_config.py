"""
Logging configuration for the application.
"""

import logging
import sys
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    enable_file_logging: bool = False,
    log_file: str = 'app.log'
) -> None:
    """Setup application logging.

    Args:
        level: Logging level (default: INFO)
        format_string: Custom format string
        enable_file_logging: Whether to also log to file
        log_file: Path to log file
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(format_string)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler (optional)
    if enable_file_logging:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(format_string)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    # Set specific levels for noisy libraries
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
