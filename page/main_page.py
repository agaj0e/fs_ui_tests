from playwright.sync_api import Page, expect

import re

from page.base_page import BasePage
from page.login_page import LoginPage
from page.search_results_page import SearchResultsPage


class MainPage(BasePage):
    """Page Object главной страницы https://fstravel.com/."""

    PATH = "/"

    def __init__(self, page: Page, base_url: str, timeout_ms: int = 15000):
        super().__init__(page, base_url, timeout_ms)

        # Шапка и профиль пользователя
        self.logo = page.get_by_role("link").filter(has=page.get_by_alt_text("logo"))
        self.profile_icon = page.locator("div.profile-menu__icon-wrapper .account-icon").first
        self.account_avatar = page.locator(".v-account-img")

        # Поисковая форма
        self.hero_heading = page.get_by_role("heading", name="Умный выбор для яркого отдыха")
        self.tours_tab = page.get_by_role("tab", name="Туры").first
        self.hotels_tab = page.get_by_role("tab", name="Отели").first
        self.exotic_tours_tab = page.get_by_role("tab", name="Экс. туры").first
        self.departure_input = page.get_by_role("textbox", name="Откуда")
        self.destination_input = page.get_by_role("textbox", name="Город, отель или страна")
        self.search_button = page.get_by_role("button", name="Найти").first

        # Контентные блоки главной страницы
        self.actions_heading = page.get_by_role("heading", name="Подборка акций")
        self.more_actions_link = page.get_by_role("link", name="Больше акций")
        self.destinations_heading = page.get_by_role("heading", name="Популярные направления")
        self.turkey_destination = page.locator('a[href*="/turkey"]').first

        # Меню авторизованного пользователя
        self.profile_link = page.get_by_role("link", name="Профиль")

    def goto(self) -> "MainPage":
        """Открывает главную страницу сайта."""
        self.page.goto(self.base_url, wait_until="domcontentloaded")
        self.hero_heading.wait_for(state="visible", timeout=self.timeout_ms)
        return self

    def open_login(self) -> LoginPage:
        """Переходит на страницу входа через иконку профиля."""
        self.profile_icon.click()
        self.page.wait_for_url(re.compile(r"auth2\.fstravel\.com.*"), timeout=self.timeout_ms)
        return LoginPage(self.page, self.base_url, self.timeout_ms)

    def search_tours(self) -> SearchResultsPage:
        """Запускает поиск туров с параметрами по умолчанию на форме."""
        self.search_button.click()
        self.page.wait_for_url(re.compile(r"searchtours"), timeout=self.timeout_ms)
        return SearchResultsPage(self.page, self.base_url, self.timeout_ms)

    def switch_to_hotels_tab(self) -> "MainPage":
        """Переключает форму поиска на вкладку «Отели»."""
        self.hotels_tab.click()
        return self

    def switch_to_tours_tab(self) -> "MainPage":
        """Переключает форму поиска на вкладку «Туры»."""
        self.tours_tab.click()
        return self

    def open_popular_destination_turkey(self) -> SearchResultsPage:
        """Открывает страницу поиска туров в Турцию из блока популярных направлений."""
        self.turkey_destination.scroll_into_view_if_needed()
        self.turkey_destination.click()
        self.page.wait_for_url(re.compile(r"searchtours"), timeout=self.timeout_ms)
        return SearchResultsPage(self.page, self.base_url, self.timeout_ms)

    def open_profile(self) -> None:
        """Открывает профиль авторизованного пользователя."""
        self.profile_icon.click()
        expect(self.profile_link).to_be_visible(timeout=self.timeout_ms)
        self.profile_link.click()
        self.wait_for_dom()
        print(self.get_current_url())


    def assert_main_page_loaded(self) -> None:
        """Проверяет ключевые элементы главной страницы."""
        expect(self.page).to_have_title("Главная")
        expect(self.hero_heading).to_be_visible()
        expect(self.search_button).to_be_visible()
        expect(self.actions_heading).to_be_visible()
        expect(self.destinations_heading).to_be_visible()

    def assert_profile_icon_visible(self) -> None:
        """Проверяет видимость иконки входа в профиль (десктопная вёрстка)."""
        expect(self.profile_icon).to_be_visible()
