import re

import pytest

from page.main_page import MainPage


@pytest.mark.smoke
@pytest.mark.search
def test_search_tours_from_main_form(main_page: MainPage):
    """Проверяет поиск туров через кнопку «Найти» на главной странице."""
    main_page.goto()
    results_page = main_page.search_tours()
    results_page.assert_tours_search_opened()
    results_page.assert_page_has_title()


@pytest.mark.search
def test_open_turkey_from_popular_destinations(main_page: MainPage):
    """Проверяет переход к турам в Турцию из блока популярных направлений."""
    main_page.goto()
    results_page = main_page.open_popular_destination_turkey()
    results_page.assert_tours_search_opened()
    assert "turkey" in results_page.get_current_url()


@pytest.mark.search
def test_hotels_tab_navigation(main_page: MainPage):
    """Проверяет переход на страницу поиска отелей через вкладку формы."""
    main_page.goto()
    main_page.switch_to_hotels_tab()
    main_page.page.wait_for_url(re.compile(r"searchhotel"), timeout=main_page.timeout_ms)
