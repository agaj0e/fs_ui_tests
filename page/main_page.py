from playwright.sync_api import Page, expect


class MainPage:
    URL = "https://fstravel.com/"

    def __init__(self, page: Page):
        self.page = page
        self.user_icon = page.locator('.v-icon-user-14')
        self.auth_popup = page.locator('.popup-auth-new').first
        self.email_input = self.auth_popup.locator('#email')
        self.password_input = self.auth_popup.locator('#password')
        self.account_avatar = page.locator('.v-account-img')
        self.profile_link = page.get_by_role("link", name="Профиль")
        self.error_message = page.get_by_text("Введен неверный логин или пароль")

    def goto(self):
        self.page.goto(self.URL, wait_until='domcontentloaded')

    def open_auth_popup(self):
        self.user_icon.click()
        self.auth_popup.wait_for(state='visible')

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.password_input.press('Enter')

    def open_profile(self):
        self.account_avatar.click()
        self.profile_link.click()
        self.page.wait_for_load_state('domcontentloaded')

