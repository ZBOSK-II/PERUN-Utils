import configparser
from pathlib import Path

from config.models import AppConfig
from config.models import AppSettings


def load_config(config: Path, profile: str) -> AppConfig:
    parser = configparser.ConfigParser()

    try:
        if config.exists():
            parser.read(config)
    except Exception:
        print("Invalid config file")
        exit(1)

    try:
        section = parser[profile]
    except Exception:
        print("Given profile not found in config file.")
        exit(1)

    command_marker = section.get("command_marker", fallback="COMMAND_START_MARKER")

    command_size = section.getint("command_size", fallback=4098)

    command_client_exe = Path(
        section.get("command_client_exe", fallback="command_client.exe")
    )

    return AppConfig(
        command_marker=command_marker,
        command_size=command_size,
        command_client_exe=command_client_exe,
    )


def load_settings() -> AppSettings:
    return AppSettings()
