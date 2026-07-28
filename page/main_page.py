from playwright.sync_api import Page, expect


class MainPage:
    URL = "https://fstravel.com/"
    AUTH_URL = "https://auth2.fstravel.com/"

    def __init__(self, page: Page):
        self.page = page
        self.user_icon = page.locator("div.profile-menu__icon-wrapper .account-icon")
        self.email_input = self.page.locator('#email')
        self.login_banner = page.get_by_role("heading", name="Войдите в профиль")
        self.password_input = self.page.locator('#password')
        self.account_avatar = page.locator('.v-account-img')
        self.profile_link = page.get_by_role("link", name="Профиль")
        self.error_message = page.get_by_text("Введен неверный логин или пароль")

    def goto(self):
        self.page.goto(self.URL, wait_until='domcontentloaded')

    def open_login_page(self):
        """Клик по иконке + ожидание загрузки формы"""
        with self.page.expect_navigation(timeout=15000):
            self.user_icon.click()
        self.login_banner.wait_for(state="visible", timeout=10000)

    def login(self, email: str, password: str):
        self.page.fill('input[name="LoginInput.Email"]', email)
        self.page.fill('input[name="LoginInput.Password"]', password)
        self.page.click('#login-submit')

    def open_profile(self):
        self.account_avatar.click()
        self.profile_link.click()
        self.page.wait_for_load_state('domcontentloaded')


    def open_login_via_icon(self):
        """Клик по иконке и переход на страницу авторизации"""
        with self.page.expect_navigation(timeout=10000):
            self.user_icon.click()
        # Ждём, что форма входа загрузилась
        self.login_banner.wait_for(state="visible", timeout=10000)