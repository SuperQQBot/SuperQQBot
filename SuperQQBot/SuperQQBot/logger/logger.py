# webhook_sdk/core/logger.py
import logging
from .logging_config import LoggerConfig
from SuperQQBot.utils.utils import sanitize_data

class WebHookLogger:
    """单例日志记录器，支持多模块统一调用"""

    _instance = None

    def __new__(cls, config: LoggerConfig = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config: LoggerConfig = None):
        if self._initialized:
            return

        self.config = config or LoggerConfig()
        self.logger = self._setup_logger()
        self._initialized = True

    def _setup_logger(self):
        """初始化日志配置"""
        logger = logging.getLogger("webhook_sdk")
        logger.setLevel(self.config.level)

        # 控制台输出
        if self.config.console_output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self._create_formatter())
            logger.addHandler(console_handler)

        # 文件输出
        if self.config.file_output:
            file_handler = logging.FileHandler(self.config.log_file)
            file_handler.setFormatter(self._create_formatter())
            logger.addHandler(file_handler)

        return logger

    def _create_formatter(self):
        """创建日志格式器"""
        if self.config.json_format:
            from pythonjsonlogger import jsonlogger
            return jsonlogger.JsonFormatter(
                fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
            )
        else:
            return logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

    def log(self, level: str, message: str, extra: dict = None):
        """通用日志方法"""
        level_map = {
            "debug": self.logger.debug,
            "info": self.logger.info,
            "warning": self.logger.warning,
            "error": self.logger.error,
            "critical": self.logger.critical
        }

        if extra and self.config.sanitize:
            extra = sanitize_data(extra)

        level_map.get(level.lower(), self.logger.info)(
            message, extra=extra
        )

    # 快捷方法
    def debug(self, message: str, extra: dict = None):
        self.log("debug", message, extra)

    def info(self, message: str, extra: dict = None):
        self.log("info", message, extra)

    def warning(self, message: str, extra: dict = None):
        self.log("warning", message, extra)

    def error(self, message: str, extra: dict = None):
        self.log("error", message, extra)
