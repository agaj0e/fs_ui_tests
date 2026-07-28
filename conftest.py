import pytest
from playwright.sync_api import Page, sync_playwright

from config.settings import Settings, get_settings
from page.main_page import MainPage


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Фикстура сессии: загружает настройки окружения один раз на прогон."""
    return get_settings()


@pytest.fixture(scope="function")
def page(settings: Settings) -> Page:
    """
    Фикстура браузера: создаёт Chromium с десктопным viewport.
    Блокирует рекламные/трекинговые домены для стабильности UI-тестов.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=settings.headless,
            args=["--headless=new"] if settings.headless else [],
        )
        context = browser.new_context(
            viewport={
                "width": settings.viewport_width,
                "height": settings.viewport_height,
            },
            locale="ru-RU",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            permissions=[],
        )
        page_obj = context.new_page()
        page_obj.set_default_timeout(settings.default_timeout_ms)

        def block_unwanted_requests(route, request):
            url = request.url
            blocked_domains = (
                "flocktory.com",
                "flockapi",
                "adriver.ru",
                "doubleclick.net",
            )
            if any(domain in url for domain in blocked_domains):
                route.abort()
            else:
                route.continue_()

        page_obj.route("**/*", block_unwanted_requests)
        page_obj.on("dialog", lambda dialog: dialog.dismiss())

        yield page_obj

        context.close()
        browser.close()


@pytest.fixture
def main_page(page: Page, settings: Settings) -> MainPage:
    """Готовый Page Object главной страницы."""
    return MainPage(page, settings.base_url, settings.default_timeout_ms)
