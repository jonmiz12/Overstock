import string
from typing import Dict

from pages.overstock.header import Header
from playwright.sync_api import Page


class ResultsPage(Header):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.results_items = page.locator("[class^=_productGrid]> ul>li")
        self.item_price = page.locator("[class^='_priceWrapper'] div[class^='_price']:nth-child(1)")
        self.item_name = page.locator("[class^='_highlighter']")

    def click_item(self, index: int):
        self.results_items.nth(index).click()

    def return_item_data(self, index: int) -> [string]:
        name = self.item_name.nth(index).text_content()
        price_text = self.item_price.nth(index).text_content()
        clean_text = self.return_clean_text(price_text, "$")
        minus_dollar = clean_text.replace("$", "")
        raw_price = float(minus_dollar)
        price = round(raw_price, 2)
        data: Dict = {
            'name': name,
            'raw_price': price,
        }
        return data

    @staticmethod
    def add_commas_to_currency(amount: str) -> str:
        number = float(amount.replace("$", ""))
        formatted_number = "{:,.2f}".format(number)
        return formatted_number
