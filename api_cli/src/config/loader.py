import configparser
from pathlib import Path

from api.exceptions import AppError
from config.models import AppConfig, AppSettings


def load_config(config: Path, profile: str) -> AppConfig:
    parser = configparser.ConfigParser()

    try:
        if config.exists():
            parser.read(config)
    except Exception as e:
        raise AppError("Given profile not found in config file") from e

    try:
        section = parser[profile]
    except Exception as e:
        raise AppError("Given profile not found in config file") from e

    default_plugins = [
        h.strip() for h in section.get("plugins", fallback="").split(",")
    ]
    timeout = section.getfloat("timeout", fallback=30.0)

    default_template_name = section.get("template")

    return AppConfig(default_plugins, timeout, default_template_name)


def load_settings() -> AppSettings:
    return AppSettings()
