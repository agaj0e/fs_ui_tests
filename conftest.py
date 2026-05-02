import pytest
from playwright.sync_api import sync_playwright, Page
import requests


@pytest.fixture(scope="function")
def page() -> Page:
    with sync_playwright() as p:
        def block_flocktory(route):
            url = route.request.url
            if "flocktory.com" in url or "flockapi" in url:
                route.abort()
            else:
                route.continue_()

        browser = p.chromium.launch(headless=False)
        context = browser.new_context(permissions=[])
        page_obj = context.new_page()
        page_obj.route("**/*", block_flocktory)
        page_obj.on("dialog", lambda dialog: dialog.dismiss())

        yield page_obj

        context.close()
        browser.close()




@pytest.fixture(scope="session")
def api_session():
    """
    Фикстура уровня сессии: создаёт requests.Session(),
    получает XSRF-токен и устанавливает нужные заголовки.
    Используется всеми тестами, которым нужна авторизация/CSRF.
    """
    session = requests.Session()

    # Убираем лишние пробелы в URL!
    resp = session.get("https://fstravel.com/")
    if resp.status_code != 200:
        raise RuntimeError(f"Не удалось загрузить главную страницу: {resp.status_code}")

    xsrf_token = session.cookies.get("XSRF-TOKEN")
    if not xsrf_token:
        raise RuntimeError("XSRF-TOKEN не найден в cookies после GET /")

    # Устанавливаем постоянные заголовки для всех запросов этой сессии
    session.headers.update({
        "x-xsrf-token": xsrf_token,
        "x-csrf-token": xsrf_token,
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    })

    return session