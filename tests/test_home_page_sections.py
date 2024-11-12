from overstock.pages.home_page import HomePage

def test_home_page_sections(page, data):
    sections_count = data["sections_count"]
    url = data["url"]

    page.goto(url)

    # home page
    home_page = HomePage(page)
    page.wait_for_load_state()
    home_page.close_dialog()
    home_page.validate_home_page_sections(sections_count)
