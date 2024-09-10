import time
from typing import List

from playwright.sync_api import Page
from pages.overstock.header import Header


class CartPage(Header):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.item_els = page.locator("#cart-items tbody>tr")
        self.item_name = page.locator(".cart-item__title")
        self.item_price = page.locator(".cart-item__info .price__current")
        self.item_total_price = page.locator(".cart-item__total .price__current")
        self.total_items_price = page.locator(".cart__summary .justify-between>p")
        self.item_quantity = page.locator("[id^='quantity']")
        self.item_quantity = page.locator("[id^='quantity']")
        self.decrease_quantity = page.locator(".cart-item__qty [name='minus']")
        self.increase_quantity = page.locator(".cart-item__qty [name='plus']")
        self.cart_page_title = page.locator(".js-cart-title")

    def validate_items_in_cart(self, cart: List[dict]):
        time.sleep(1)
        self.validate_cart(cart, self.item_els, self.item_name, self.item_quantity, self.item_price,
                           self.item_total_price)

    def validate_total_price(self, cart: List[dict]):
        expected_total = 0

        for item in cart:
            price = item["raw_price"] * float(item["quantity"])
            expected_total = expected_total + price

        expected_total = int(expected_total)

        price_text = self.total_items_price.inner_text()

        minus_dollar = self.return_clean_text(price_text, "$", True)

        minus_usd = float(minus_dollar.replace(" USD", ""))

        actual_total_price = int(minus_usd)

        assert expected_total == actual_total_price

    def wait_for_cart_page(self):
        self.cart_page_title.wait_for()
        assert self.cart_page_title.inner_text() == "Your cart"
