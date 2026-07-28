import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Настройки тестового окружения, загружаемые из переменных среды."""

    base_url: str
    auth_url: str
    email: str
    password: str
    invalid_email: str
    invalid_password: str
    headless: bool
    viewport_width: int
    viewport_height: int
    default_timeout_ms: int

    @property
    def has_valid_credentials(self) -> bool:
        """Проверяет, заданы ли учётные данные для позитивных тестов авторизации."""
        return bool(self.email and self.password)


def get_settings() -> Settings:
    """Возвращает объект настроек с значениями по умолчанию для fstravel.com."""
    return Settings(
        base_url=os.getenv("BASE_URL", "https://fstravel.com/").rstrip("/") + "/",
        auth_url=os.getenv("AUTH_URL", "https://auth2.fstravel.com/"),
        email=os.getenv("EMAIL", ""),
        password=os.getenv("PASSWORD", ""),
        invalid_email=os.getenv("INVALID_EMAIL", "invalid@test.com"),
        invalid_password=os.getenv("INVALID_PASSWORD", "WrongPass123!"),
        headless=os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes"},
        viewport_width=int(os.getenv("VIEWPORT_WIDTH", "1920")),
        viewport_height=int(os.getenv("VIEWPORT_HEIGHT", "1080")),
        default_timeout_ms=int(os.getenv("DEFAULT_TIMEOUT_MS", "15000")),
    )
