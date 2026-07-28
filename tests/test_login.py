from page.main_page import MainPage
from playwright.sync_api import expect

def test_main_page_loads(page):
    main_page = MainPage(page)
    main_page.goto()
    expect(main_page.user_icon).to_be_visible()


def test_open_login(page):
    main_page = MainPage(page)
    main_page.goto()
    main_page.open_login_page()
    assert main_page.email_input.is_visible()
    # assert main_page.password_input.is_visible()
    # assert "auth2.fstravel.com" in page.url

def test_login_valid(page):
    main_page = MainPage(page)
    main_page.goto()
    main_page.open_auth_popup()
    main_page.login()
    main_page.open_profile()
    expect(page.get_by_text("Путешествия")).to_be_visible()


def test_login_invalid_mail(page, creds):
    main_page = MainPage(page)
    main_page.goto()
    main_page.login(creds.valid_mail, creds.valid_password)
    expect(main_page.error_message).to_be_visible()

def test_login_invalid_pass(page, creds):
    main_page = MainPage(page)
    main_page.goto()
    main_page.login(creds.valid_mail, creds.invalid_password)
    expect(main_page.error_message).to_be_visible()