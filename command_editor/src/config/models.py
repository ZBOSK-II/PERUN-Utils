from dataclasses import dataclass
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


@dataclass
class AppConfig:
    command_marker: str
    command_size: int
    command_client_exe: Path


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    config_file: Path = Path(".config")
    profile: str = "default"


@dataclass
class AppArgs:
    command_marker: str
    command_size: int
    command_client_exe: Path
    command_file: Path
    output_file: Path
