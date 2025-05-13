import inspect
import json
import string
import time
from asyncio import wait_for

from overstock.pages.header import Header
from playwright.sync_api import Page

from overstock.pages.home_page import HomePage
from utils.utils import Utils


class ResultsPage(Header):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        locators_path = Utils.convert_to_locators_directory(__file__)
        with open(locators_path, "r") as file:
            locators = json.load(file)
        for key, value in locators.items():
            setattr(self, key, page.locator(value))

    def click_item(self, index: int):
        homepage = HomePage(self.page)
        time.sleep(3)
        homepage.close_dialog()
        self.results_items.nth(index).click()

    def return_item_data(self, index: int) -> dict[str, str | int | float]:
        self.close_dialog()
        self.results_summary.wait_for()
        vendor = self.item_vendor.nth(index).inner_text()
        vendor_clean_text = vendor.replace("by ", "")

        name = self.item_name.nth(index).text_content()

        price_text = self.item_price.nth(index).text_content()
        clean_text = self.extract_clean_text(price_text, "$", True)
        raw_price = float(clean_text)
        price = round(raw_price, 2)

        data: dict = {
            'name': name,
            'raw_price': price,
            'vendor': vendor_clean_text
        }
        return data

    @staticmethod
    def add_commas_to_currency(amount: str) -> str:
        number = float(amount.replace("$", ""))
        formatted_number = "{:,.2f}".format(number)
        return formatted_number

    def assert_title(self, query: str):
        title = None
        try:
            title = self.search_title.inner_text(timeout=3000)
        except Exception:
            pass
        if title != query or title is None:
            self.get_screenshot_in_test_report()
            self.add_failed_assertion(f"query: {query}, title: {title}", inspect.currentframe().f_code.co_name)
