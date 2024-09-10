from playwright.sync_api import Page
from pages.overstock.basePage import BasePage


class Header(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.search_box = page.locator("[role='textbox']")
        self.search_btn = page.locator(".header-search-global [type='submit']")
        self.cart_btn = page.locator("#cart-icon")
        self.cart_num = page.locator(".header__cart-count>span:nth-child(1)")

    def search_for(self, query: str):
        self.search_box.click()
        self.search_box.fill(query)
        self.search_btn.click()

    def click_cart(self):
        self.cart_btn.click()

    def extract_cart_num(self) -> int:
        string_number = self.cart_num.inner_text()
        num = int(string_number)
        return num
