import re

from playwright.sync_api import Page, expect

from page.base_page import BasePage


class SearchResultsPage(BasePage):
    """Page Object страницы результатов поиска туров."""

    def __init__(self, page: Page, base_url: str, timeout_ms: int = 15000):
        super().__init__(page, base_url, timeout_ms)

        # На странице результатов обычно есть фильтры и список предложений
        self.page_heading = page.locator("h1").first

    def assert_tours_search_opened(self) -> None:
        """Проверяет переход на страницу поиска туров."""
        expect(self.page).to_have_url(re.compile(r"searchtours"))

    def assert_hotels_search_opened(self) -> None:
        """Проверяет переход на страницу поиска отелей."""
        expect(self.page).to_have_url(re.compile(r"searchhotel"))

    def assert_page_has_title(self) -> None:
        """Проверяет, что у страницы задан заголовок (не пустой)."""
        title = self.page.title()
        assert title, "Заголовок страницы результатов поиска не должен быть пустым"
