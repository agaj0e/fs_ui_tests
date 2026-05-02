# tests/test_auth.py
from page.main_page import MainPage
from dotenv import load_dotenv
import os
from playwright.sync_api import expect

load_dotenv()

valid_mail = os.getenv("EMAIL")
valid_password = os.getenv("PASSWORD")
base_url = os.getenv("BASE_URL")
invalid_password = os.getenv("INVALID_PASSWORD")
invalid_mail = os.getenv("INVALID_EMAIL")


def test_main_page_loads(page):
    main_page = MainPage(page)
    main_page.goto()



def test_open_login_popup(page):
    main_page = MainPage(page)
    main_page.goto()
    main_page.open_auth_popup()
    assert main_page.auth_popup.is_visible()


def test_login_valid(page):
    main_page = MainPage(page)
    main_page.goto()
    main_page.open_auth_popup()
    main_page.login(valid_mail, valid_password)
    main_page.open_profile()
    expect(page.get_by_text("Путешествия")).to_be_visible()


def test_login_invalid_mail(page):
    main_page = MainPage(page)
    main_page.goto()
    main_page.open_auth_popup()
    main_page.login(invalid_mail, valid_password)
    expect(main_page.error_message).to_be_visible()

def test_login_invalid_pass(page):
    main_page = MainPage(page)
    main_page.goto()
    main_page.open_auth_popup()
    main_page.login(valid_mail, invalid_password)
    expect(main_page.error_message).to_be_visible()