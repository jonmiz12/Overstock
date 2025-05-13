import json

from playwright.sync_api import Page
from overstock.pages.header import Header
from overstock.pages.cart_page import CommonCart
from utils.utils import Utils


class CartDrawer(Header, CommonCart):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        locators_path = Utils.convert_to_locators_directory(__file__)
        with open(locators_path, "r") as file:
            locators = json.load(file)
        for key, value in locators.items():
            setattr(self, key, page.locator(value))

    def wait_for_drawer(self):
        self.checkout_button.wait_for()

    def click_cart_close_button(self):
        self.cart_drawer_close_button.click()

    def validate_items_in_cart(self, cart: list[dict[str, str | int | float]]):
        self.validate_cart(cart, self.item_els, self.item_name, self.item_quantity, self.item_price, self.item_total_price)

    def click_cart_page_button(self):
        self.cart_page_button.click()

    def get_quantity_by_name_cart_drawer(self, expected_name) -> int:
        return self.get_quantity_by_name(expected_name, self.item_els, self.item_quantity, self.item_name)

    def change_cart_quantities_cart_drawer(self, cart: list[dict[str, str | int | float]], amounts: [int]) -> list[dict[str, str | int | float]]:
        cart = self.change_cart_quantities(self, cart, amounts, self.item_els, self.item_name, self.increase_quantity,
                                           self.decrease_quantity, self.item_quantity, self.item_error, self.cart_button)
        return cart

    def remove_item_cart_drawer(self, item: dict[str, str | int | float], cart: list[dict[str, str | int | float]]) -> list[dict[str, str | int | float]]:
        cart = self.remove_item(item, cart, self.item_els, self.item_name, self.remove_button)
        return cart

    def remove_multiple_items(self, cart, remove_indexes: [int]):
        for index in remove_indexes:
            self.remove_item_cart_drawer(cart[remove_indexes[index]], cart)
            self.check_for_discount_and_update_cart(cart)
            self.validate_items_in_cart(cart)
