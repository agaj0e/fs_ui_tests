import re

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--headless=new"])
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="ru-RU",
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    )
    page = context.new_page()
    page.goto("https://fstravel.com/", wait_until="domcontentloaded")
    page.locator("h1").first.wait_for()

    link = page.locator('a[href*="/turkey"]').first
    print("turkey count", link.count())
    link.scroll_into_view_if_needed()
    link.click()
    page.wait_for_timeout(5000)
    print("after turkey url", page.url)
    print("after turkey title", repr(page.title()))

    page.goto("https://fstravel.com/", wait_until="domcontentloaded")
    page.locator("h1").first.wait_for()
    icon = page.locator("div.profile-menu__icon-wrapper .account-icon").first
    icon.wait_for()
    icon.click()
    page.wait_for_timeout(5000)
    print("after login click url", page.url)

    browser.close()
