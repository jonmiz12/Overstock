import json

from playwright.sync_api import Page
from overstock.base_page import BasePage
from utils.utils import Utils


class Header(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        locators_path = Utils.convert_to_locators_directory(__file__)
        with open(locators_path, "r") as file:
            locators = json.load(file)
        for key, value in locators.items():
            setattr(self, key, page.locator(value))

    def search_for(self, query: str):
        self.search_box.click()
        self.search_box.fill(query)
        self.search_button.click()

    def click_cart(self):
        self.cart_button.click()

    def extract_cart_num(self) -> int:
        string_number = self.cart_num.inner_text()
        num = int(string_number)
        return num

    def close_dialog(self):
        if self.close_discount_dialog.is_visible():
            self.close_discount_dialog.click()
        for button in self.close_dialog_button.all():
            if button.is_visible():
                button.click(timeout=500)
                break
