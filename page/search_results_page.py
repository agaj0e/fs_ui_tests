import re

from playwright.sync_api import Page

from page.base_page import BasePage


class SearchResultsPage(BasePage):
    """Page Object страницы результатов поиска туров."""

    def __init__(self, page: Page, base_url: str, timeout_ms: int = 15000):
        super().__init__(page, base_url, timeout_ms)

        # На странице результатов обычно есть фильтры и список предложений
        self.page_heading = page.locator("h1").first

    def assert_tours_search_opened(self) -> None:
        """Проверяет, что открыта страница поиска туров."""
        self.expect_url_contains("searchtours")

    def assert_page_has_title(self) -> None:
        """Проверяет наличие заголовка на странице результатов."""
        self.page_heading.wait_for(state="visible", timeout=self.timeout_ms)
