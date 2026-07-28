import re

from playwright.sync_api import Page, expect


class BasePage:
    """Базовый класс Page Object Model для всех страниц сайта."""

    def __init__(self, page: Page, base_url: str, timeout_ms: int = 15000):
        self.page = page
        self.base_url = base_url
        self.timeout_ms = timeout_ms
        self.page.set_default_timeout(timeout_ms)

    def wait_for_dom(self) -> None:
        """Ожидает загрузку DOM текущей страницы."""
        self.page.wait_for_load_state("domcontentloaded")

    def get_current_url(self) -> str:
        """Возвращает текущий URL страницы."""
        return self.page.url

    def expect_url_contains(self, fragment: str) -> None:
        """Проверяет, что URL содержит указанный фрагмент."""
        expect(self.page).to_have_url(re.compile(re.escape(fragment)))
