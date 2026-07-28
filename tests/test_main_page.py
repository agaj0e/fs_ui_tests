import re

import pytest
from playwright.sync_api import expect

from config.settings import Settings


@pytest.mark.smoke
def test_main_page_loads(main_page):
    """Проверяет загрузку главной страницы и ключевых блоков."""
    main_page.goto()
    main_page.assert_main_page_loaded()


@pytest.mark.smoke
def test_profile_icon_visible(main_page):
    """Проверяет видимость иконки профиля в десктопной вёрстке."""
    main_page.goto()
    main_page.assert_profile_icon_visible()


@pytest.mark.smoke
def test_main_page_sections_visible(main_page):
    """Проверяет наличие блоков акций и популярных направлений."""
    main_page.goto()

    expect(main_page.actions_heading).to_be_visible()
    expect(main_page.more_actions_link).to_be_visible()
    expect(main_page.destinations_heading).to_be_visible()
    expect(main_page.turkey_destination).to_be_visible()


@pytest.mark.smoke
def test_search_form_tabs(main_page):
    """Проверяет переключение вкладок формы поиска."""
    main_page.goto()

    expect(main_page.tours_tab).to_be_visible()
    expect(main_page.hotels_tab).to_be_visible()

    main_page.switch_to_hotels_tab()
    expect(main_page.page).to_have_url(re.compile(r"searchhotel"))

    main_page.goto()
    main_page.switch_to_tours_tab()
    expect(main_page.search_button).to_be_visible()
