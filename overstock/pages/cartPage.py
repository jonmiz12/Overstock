import inspect
from typing import List

from playwright.sync_api import Page
from overstock.pages.header import Header
from overstock.commonCart import CommonCart


class CartPage(Header, CommonCart):

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
        self.remove_button = page.locator(".cart-item__remove")
        self.item_error = page.locator("[id^='line-item-error']")
        self.item_vendor = page.locator(".cart-item__details .text-theme-light")

    def validate_items_in_cart(self, cart: List[dict]):
        self.validate_cart(cart, self.item_els, self.item_name, self.item_vendor, self.item_quantity, self.item_price,
                           self.item_total_price)

    def validate_total_price(self, cart: List[dict]):
        expected_total_price = 0
        for item in cart:
            price = item["raw_price"] * float(item["quantity"])
            expected_total_price = expected_total_price + price
        expected_total_price = int(expected_total_price)
        price_text = self.total_items_price.inner_text()
        minus_dollar = self.extract_clean_text(price_text, "$", True)
        minus_usd = float(minus_dollar.replace(" USD", ""))
        actual_total_price = int(minus_usd)
        if expected_total_price != actual_total_price:
            self.get_screenshot_in_test_report()
            self.add_failed_assertion(f"actual total price: {actual_total_price}. expected total price: {expected_total_price}\nfor cart: {cart}", inspect.currentframe().f_code.co_name)

    def wait_for_cart_page(self):
        self.cart_page_title.wait_for()
        actual_title = self.cart_page_title.inner_text()
        expected_title = "Your cart"
        if self.cart_page_title.inner_text() == expected_title:
            self.get_screenshot_in_test_report()
            self.add_failed_assertion(f"actual title: {actual_title}. expected title: {expected_title}", inspect.currentframe().f_code.co_name)

    def remove_item_cart_page(self, item: dict, cart: List[dict]):
        self.remove_item(item, cart, self.item_els, self.item_name, self.remove_button)

    def change_cart_quantities_cart_page(self, cart: List[dict], amounts: [int]) -> List[dict]:
        cart = self.change_cart_quantities(self, cart, amounts, self.item_els, self.item_name, self.increase_quantity,
                                           self.decrease_quantity, self.item_quantity, self.item_error, self.cart_btn)
        return cart
