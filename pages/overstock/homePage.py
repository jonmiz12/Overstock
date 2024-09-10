from pages.overstock.header import Header
from playwright.sync_api import Page, expect


class HomePage(Header):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.close_dialog_btn = page.locator("#cl-dialog-close")
        self.topics_small_headers = page.locator(".section__header")
        self.topics_big_headers = page.locator(".block-section-title")

    def close_dialog(self):
        self.close_dialog_btn.click()

    def validate_home_page_topics(self):
        expect(self.topics_small_headers.is_visible())
        expect(self.topics_big_headers.is_visible())
