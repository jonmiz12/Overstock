from playwright.sync_api import Page, expect

from pages.wikipedia import Wikipedia


def test_wiki_expand_contents(page: Page):
    page.goto("https://www.wikipedia.org/")
    wiki = Wikipedia(page)

    wiki.search_for("israel")
    wiki.wait_for_page_to_load()
    wiki.click_expand_btns()
