import string

import locator as locator
from playwright.sync_api import Page, expect


class Wikipedia:
    page: Page
    wiki_logo: locator
    search_box: locator
    search_btn: locator
    topics: locator
    expandTopic_btns: locator

    def __init__(self, page: Page):
        self.page = page
        self.wiki_logo = page.locator(".central-textlogo-wrapper > .central-textlogo__image")
        self.search_box = page.locator("#searchInput")
        self.search_btn = page.locator("[type='submit']")
        self.topics = page.locator(".vector-toc-contents > li")
        self.expandTopic_btns = page.locator(".mw-ui-icon-wikimedia-expand")

    # homepage
    def search_for(self, query: string):
        expect(self.wiki_logo).to_be_visible()
        self.search_box.fill(query)
        self.search_btn.click()

    # subject page
    # level2Items = page.locator(".vector-toc-level-2")
    def wait_for_page_to_load(self):
        self.page.wait_for_load_state("load")

    def click_expand_btns(self):
        topicsCount = self.topics.count()
        for index in range(topicsCount):
            self.expandTopic_btns.nth(index).click()
            # expect(level2Items.nth(index)).to_be_visible()
