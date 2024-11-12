import inspect
import json

from playwright.sync_api import Page
from overstock.pages.header import Header
from overstock.common_cart import CommonCart
from utils.utils import Utils


class CartPage(Header, CommonCart):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        locators_path = Utils.convert_to_locators_directory(__file__)
        with open(locators_path, "r") as file:
            locators = json.load(file)
        for key, value in locators.items():
            setattr(self, key, page.locator(value))

    def validate_items_in_cart(self, cart: list[dict[str, str | int | float]]):
        self.validate_cart(cart, self.item_els, self.item_name, self.item_vendor, self.item_quantity, self.item_price,
                           self.item_total_price)

    def validate_total_price(self, cart: list[dict[str, str | int | float]]):
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

    def remove_item_cart_page(self, item: dict[str, str | int | float], cart: list[dict[str, str | int | float]]):
        self.remove_item(item, cart, self.item_els, self.item_name, self.remove_button)

    def change_cart_quantities_cart_page(self, cart: list[dict[str, str | int | float]], amounts: [int]) -> list[dict[str, str | int | float]]:
        cart = self.change_cart_quantities(self, cart, amounts, self.item_els, self.item_name, self.increase_quantity,
                                           self.decrease_quantity, self.item_quantity, self.item_error, self.cart_button)
        return cart

    def remove_multiple_items(self, cart, remove_indexes: [int]):
        for index in remove_indexes:
            self.remove_item_cart_page(cart[remove_indexes[index]], cart)
            self.check_for_discount_and_update_cart(cart)
            self.validate_items_in_cart(cart)