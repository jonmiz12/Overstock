from playwright.sync_api import Page
from overstock.pages.homePage import HomePage


def test_home_page_sections(page: Page):
    page.goto("https://www.overstock.com/")

    # home page
    home_page = HomePage(page)
    page.wait_for_load_state()
    home_page.close_dialog()
    home_page.validate_home_page_sections()
