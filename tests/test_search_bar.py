from overstock.pages.home_page import HomePage
from overstock.pages.results_page import ResultsPage

def test_search_bar(page, data):
    query = data
    page.goto("https://www.overstock.com/")

    # home page
    home_page = HomePage(page)
    home_page.close_dialog()
    home_page.search_for(query)
    page.wait_for_load_state()
    results_page = ResultsPage(page)
    results_page.assert_title(query)
