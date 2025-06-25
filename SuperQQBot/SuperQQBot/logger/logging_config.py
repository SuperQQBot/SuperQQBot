# webhook_sdk/core/logging_config.py
from dataclasses import dataclass
from typing import Optional
import logging
@dataclass
class LoggerConfig:
    """日志配置类"""
    level: int = logging.INFO
    console_output: bool = True
    file_output: bool = False
    log_file: Optional[str] = None
    max_bytes: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    json_format: bool = False
    sanitize: bool = True  # 是否自动脱敏
