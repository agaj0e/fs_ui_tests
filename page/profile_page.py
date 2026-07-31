from playwright.sync_api import Page, expect
import re

from page.base_page import BasePage


class ProfilePage(BasePage):
    """Класс страницы профиля пользовтеля"""

    def __init__(self, page: Page, base_url: str, timeout_ms: int = 15000):
        super().__init__(page, base_url, timeout_ms)

