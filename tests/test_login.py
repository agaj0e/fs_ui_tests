import pytest
from playwright.sync_api import expect

from config.settings import Settings
from page.main_page import MainPage


@pytest.mark.smoke
@pytest.mark.login
def test_open_login_page(main_page: MainPage):
    """Проверяет переход на страницу авторизации через иконку профиля."""
    main_page.goto()
    login_page = main_page.open_login()
    login_page.assert_loaded()


@pytest.mark.login
def test_login_invalid_email(main_page: MainPage, settings: Settings):
    """Проверяет ошибку при входе с несуществующим email."""
    main_page.goto()
    login_page = main_page.open_login()
    login_page.login(settings.invalid_email, settings.invalid_password)
    login_page.assert_invalid_email_error()


@pytest.mark.login
@pytest.mark.auth_required
def test_login_invalid_password(main_page: MainPage, settings: Settings):
    """Проверяет ошибку при неверном пароле для существующего аккаунта."""
    if not settings.has_valid_credentials:
        pytest.skip("Для теста нужны EMAIL и PASSWORD в .env")

    main_page.goto()
    login_page = main_page.open_login()

    """Делаем первые 2 попытки (лимит - 3, значит первые 2 дают обычную ошибку)"""
    for attempt in range(2):
        login_page.login(settings.email, settings.invalid_password)
        login_page.assert_invalid_password_first_try()

    # Этап 2: Делаем 3-ю попытку, которая должна вызвать бан
    login_page.login(settings.email, settings.invalid_password)

    # Этап 3: Проверяем, что появилась плашка о бане на 15 минут
    # Обычная ошибка "Неверный пароль" может исчезнуть или смениться на бан
    login_page.assert_invalid_password_15minban()

@pytest.mark.login
@pytest.mark.auth_required
def test_login_valid(main_page: MainPage, settings: Settings):
    """Проверяет успешный вход и доступ к профилю пользователя."""
    if not settings.has_valid_credentials:
        pytest.skip("Для теста нужны EMAIL и PASSWORD в .env")

    main_page.goto()
    login_page = main_page.open_login()
    login_page.login(settings.email, settings.password)
    login_page.wait_for_successful_login()

    expect(main_page.account_avatar).to_be_visible(timeout=settings.default_timeout_ms)
    main_page.open_profile()
    expect(main_page.page.get_by_text("Путешествия")).to_be_visible()


