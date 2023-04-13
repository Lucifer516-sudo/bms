# from rich.traceback import install

# install()
from pathlib import Path
from typing import Any, Literal, Mapping, Optional, Union
from colorama import Fore, Back, Style
import logging
from bms.backend.config import BMS_LOG_DIR


class CustomFormatter(logging.Formatter):
    def __init__(
        self,
        *args,
        **kwargs,
        # fmt: strfmt, datefmt, style, validate, defaults=defaults
        # | None = "(%(asctime)s) %(levelname)s `%(name)s`: %(message)s",
        # datefmt: str | None = "%d %b, %Y %I:%M:%S %p",
        # style: logging._FormatStyle = "%",
        # validate: bool = True,
        # *,
        # defaults: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            *args, **kwargs
        )  # fmt, datefmt, style, validate, defaults=defaults
        self.colors: dict[str, str] = {
            "DEBUG": Fore.GREEN,
            "INFO": Fore.YELLOW,
            "WARNING": Fore.MAGENTA,
            "ERROR": Back.YELLOW + Fore.LIGHTRED_EX,
            "CRITICAL": Back.BLUE + Fore.RED,
        }
        self.RESET = Fore.RESET

    def format(self, record: logging.LogRecord) -> str:
        level_name = record.levelname
        if level_name in self.colors:
            colorized_level_name = f"[{Style.BRIGHT}{self.colors[level_name]}{level_name:<8}{self.RESET}{Style.RESET_ALL}]"
            record.levelname = colorized_level_name
        logger_name = f"{Style.BRIGHT}{record.name}{Style.RESET_ALL}"
        record.name = logger_name
        return super().format(record)


class Logger:
    def __init__(
        self,
        logger_name: str,
        logger_level: Literal[
            "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
        ] = "ERROR",
        logging_file: Optional[str] = None,
        logging_dir: Optional[Union[Path, str]] = None,
        log_to_stdout: bool = True,
    ) -> None:
        self.logger_name = logger_name
        in_built_levels: dict = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        if logger_level in list(in_built_levels.keys()):  # setting log level
            self.logger_level = in_built_levels[logger_level]

        # Creating logging directories and setting it to class members
        if logging_file != None:
            self.logging_file = str(logging_file)
        if logging_dir != None:
            self.logging_dir = Path(logging_dir)
            self.logging_dir.mkdir(parents=True, exist_ok=True)

        # Now Creating logger: Self and setting level
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.logger_level)

        if log_to_stdout == True:
            # Creating Handlers for stdout and file
            # Console handler:
            self.console_handler = logging.StreamHandler()

            # File Handler:
            self.file_handler = logging.FileHandler(
                filename=str(
                    self.logging_dir / str(self.logging_file + ".log")
                )
            )

            self.file_handler.setLevel(logging.DEBUG)
            # Set Formatters:
            # console formatter
            self.console_handler.setFormatter(
                CustomFormatter(
                    "(%(asctime)s) %(levelname)s `%(name)s`: %(message)s",
                    "%d %b, %Y %I:%M:%S %p",
                )
            )

            # File handler
            self.file_handler.setFormatter(
                logging.Formatter(
                    "(%(asctime)s) %(levelname)s `%(name)s`: %(message)s",
                )
            )

            # Adding both the formatted handlers to the logger
            self.logger.addHandler(self.console_handler)  # console handler
            self.logger.addHandler(self.file_handler)  # file handler
        else:
            # Creating Handlers for file
            # File Handler:
            self.file_handler = logging.FileHandler(
                filename=str(
                    self.logging_dir / str(self.logging_file + ".log")
                )
            )

            self.file_handler.setLevel(logging.DEBUG)
            # Set Formatter:
            # File handler
            self.file_handler.setFormatter(
                logging.Formatter(
                    "(%(asctime)s) %(levelname)s `%(name)s`: %(message)s",
                )
            )

            # Adding both the formatted handlers to the logger
            self.logger.addHandler(self.file_handler)  # file handler

    def change_logger_name(self, new_name: str) -> bool:
        try:
            self.logger.name = new_name
        except Exception as e:
            print("Cant change the logger name", "\n", "Error: ", e)

    def debug(self, message, *args, **kwargs):
        """Log a debug message."""
        self.logger.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        """Log an info message."""
        self.logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """Log a warning message."""
        self.logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        """Log an error message."""
        self.logger.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        """Log a critical message."""
        self.logger.critical(message, *args, **kwargs)

    def exception(self, message, *args, exc_info=True, **kwargs):
        """Log an exception message."""
        self.logger.exception(message, *args, exc_info=exc_info, **kwargs)
