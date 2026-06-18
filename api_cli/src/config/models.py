from dataclasses import dataclass
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


@dataclass
class AppConfig:
    default_plugins: list[str]
    timeout: float = 30.0


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_url: str | None = None
    token: str | None = None

    profile: str = "default"
    config_file: Path = Path(".config")


@dataclass
class ApiArgs:
    timeout: float
    api_url: str
    token: str
