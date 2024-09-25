import pytest
from playwright.sync_api import Page

from utils.utils import Utils
from overstock.pages.homePage import HomePage
from overstock.pages.resultsPage import ResultsPage

data = Utils.extract_json("search_queries.json")


@pytest.mark.parametrize("param", data)
def test_search(page: Page, param):
    query = param
    page.goto("https://www.overstock.com/")

    # home page
    home_page = HomePage(page)
    home_page.close_dialog()
    home_page.search_for(query)
    page.wait_for_load_state()
    results_page = ResultsPage(page)
    results_page.assert_title(query)
