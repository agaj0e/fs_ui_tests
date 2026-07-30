from playwright.sync_api import Page, expect
import re

from page.base_page import BasePage


class LoginPage(BasePage):
    """Page Object страницы авторизации https://auth2.fstravel.com/."""

    def __init__(self, page: Page, base_url: str, timeout_ms: int = 15000):
        super().__init__(page, base_url, timeout_ms)

        self.login_heading = page.get_by_role("heading", name="Войдите в профиль")
        self.email_input = page.locator('input[name="LoginInput.Email"]')
        self.password_input = page.locator('input[name="LoginInput.Password"]')
        self.submit_button = page.locator("#login-submit").first
        self.register_link = page.get_by_role("link", name="Зарегистрироваться")

        # Сообщения об ошибках авторизации
        self.invalid_credentials_error = page.get_by_text("Введен неверный логин или пароль")
        self.invalid_password_first_try = self.page.get_by_text(re.compile(r"Неверный\s+пароль"))
        self.invalid_password_15min_ban = self.page.get_by_text(re.compile(r"15\s*минут"))
        self.email_not_found_error = page.get_by_text(
            "Аккаунта с таким Email не существует - пожалуйста зарегистрируйтесь"
        )

    def assert_loaded(self) -> None:
        """Проверяет, что форма входа отображается."""
        expect(self.page).to_have_title("Вход")
        expect(self.login_heading).to_be_visible()
        expect(self.email_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.submit_button).to_be_visible()

    def fill_email(self, email: str) -> "LoginPage":
        """Заполняет поле email."""
        self.email_input.fill(email)
        return self

    def fill_password(self, password: str) -> "LoginPage":
        """Заполняет поле пароля."""
        self.password_input.fill(password)
        return self

    def submit(self) -> None:
        """Отправляет форму входа."""
        self.submit_button.click()

    def login(self, email: str, password: str) -> None:
        """Выполняет полный сценарий входа с указанными учётными данными."""
        self.fill_email(email)
        self.fill_password(password)
        self.submit()

    def assert_invalid_email_error(self) -> None:
        """Проверяет сообщение об отсутствии аккаунта с указанным email."""
        expect(self.email_not_found_error).to_be_visible()

    def assert_invalid_credentials_error(self) -> None:
        """Проверяет сообщение о неверном логине или пароле."""
        expect(self.invalid_credentials_error).to_be_visible()

    def assert_invalid_password_first_try(self) -> None:
        self.page.screenshot(path="debug_login_error.png")
        expect(self.page.get_by_text("Неверный пароль")).to_be_visible(timeout=15000)

    def assert_invalid_password_15minban(self) -> None:
        """Проверяет плашку бана на 15 минут после неправильных попыток"""
        expect(self.invalid_password_15min_ban).to_be_visible(timeout=15000)

    def wait_for_successful_login(self) -> None:
        """Ожидает возврат на основной сайт после успешной авторизации."""
        self.page.wait_for_url(f"{self.base_url}**", timeout=self.timeout_ms)
