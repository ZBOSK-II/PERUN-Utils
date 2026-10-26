import configparser
from pathlib import Path

from config.models import AppConfig
from config.models import AppSettings
from api.exceptions import AppError


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

    plugins = [
        h.strip() for h in section.get("default_plugins", fallback="").split(",")
    ]
    timeout = section.getfloat("timeout", fallback=30.0)

    template_name = section.get("template_name")

    return AppConfig(plugins, timeout, template_name)


def load_settings() -> AppSettings:
    return AppSettings()
