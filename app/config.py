import os
import subprocess

from pydantic_settings import BaseSettings


def _get_static_version():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=os.path.dirname(os.path.dirname(__file__)),
        ).decode().strip()
    except Exception:
        return "dev"


class Settings(BaseSettings):
    app_name: str = "Salud Natura"
    app_tagline: str = "Sabiduría Ancestral de la Tierra"
    contact_email: str = "josepsaludnatura@gmail.com"
    database_url: str = "sqlite:///data/salud_natura.db"
    environment: str = "development"
    static_version: str = _get_static_version()

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
