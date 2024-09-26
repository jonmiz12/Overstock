import string
from typing import Dict

from overstock.pages.header import Header
from playwright.sync_api import Page


class ResultsPage(Header):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.results_items = page.locator("[class^=_productGrid]> ul>li")
        self.item_price = page.locator("[class^='_priceWrapper'] div[class^='_price']:nth-child(1)")
        self.item_name = page.locator("[class^='_highlighter']")
        self.item_vendor = page.locator("[class^='_brand']")
        self.search_title = page.locator("#sr-root>[class^='_title']")

    def click_item(self, index: int):
        self.results_items.nth(index).click()

    def return_item_data(self, index: int) -> [string]:
        vendor = self.item_vendor.nth(index).inner_text()
        vendor_clean_text = vendor.replace("by ", "")

        name = self.item_name.nth(index).text_content()

        price_text = self.item_price.nth(index).text_content()
        clean_text = self.extract_clean_text(price_text, "$", True)
        raw_price = float(clean_text)
        price = round(raw_price, 2)

        data: Dict = {
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
            self.add_failed_assertion(f"query: {query}, title: {title}")
