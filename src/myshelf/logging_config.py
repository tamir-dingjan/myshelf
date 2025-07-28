import logging
import logging.handlers
import os
from pathlib import Path


def setup_logging(
    log_file: str = "myshelf.log",
    log_level: str = "INFO",
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> None:
    """
    Set up application-wide logging configuration.

    Args:
        log_file: Name of the log file (will be created in the project root)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup log files to keep
    """
    # Create logs directory if it doesn't exist
    project_root = Path(__file__).parent.parent.parent
    logs_dir = os.path.join(project_root, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    log_file_path = os.path.join(logs_dir, log_file)

    # Convert the given log level string to logging level constant
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    log_level_constant = level_map.get(log_level.upper(), logging.INFO)

    # Format the logs with time, filename, level, and message
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Create rotating file handler to limit log file sizes and manage backups
    file_handler = logging.handlers.RotatingFileHandler(
        log_file_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setLevel(log_level_constant)
    file_handler.setFormatter(formatter)

    # Create console handler to write to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level_constant)
    console_handler.setFormatter(formatter)

    # Configure the root logger for inheritance across all libraries/modules
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level_constant)

    # Replace any existing handlers to avoid duplicate output
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Start logging
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured - File: {log_file_path}, Level: {log_level}")


def get_logger(name: str) -> logging.Logger:
    # Get a logger instance for the given name
    return logging.getLogger(name)
