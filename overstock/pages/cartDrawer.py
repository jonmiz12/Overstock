import time
from typing import List

from playwright.sync_api import Page
from overstock.pages.header import Header
from overstock.pages.cartPage import CommonCart


class CartDrawer(Header, CommonCart):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.drawer_el = page.locator("cart-drawer.drawer")
        self.item_els = page.locator(".cart-items tbody>tr")
        self.item_name = page.locator(".cart-item__title")
        self.item_price = page.locator(".cart-item__info .price__current")
        self.item_total_price = page.locator(".cart-item__total .price__current")
        self.item_quantity = page.locator("[id^='quantity']")
        self.cart_drawer_clos_btn = page.locator("cart-drawer .drawer__close-btn")
        self.cart_page_btn = page.locator(".cart-drawer__view-cart")
        self.decrease_quantity = page.locator(".cart-item__qty [name='minus']")
        self.increase_quantity = page.locator(".cart-item__qty [name='plus']")
        self.remove_button = page.locator(".cart-item__remove")
        self.item_error = page.locator("[id^='line-item-error']")
        self.item_vendor = page.locator(".cart-item__details .text-theme-light")
        self.checkout_btn = page.locator("button[name='checkout']")

    def wait_for_drawer(self):
        self.checkout_btn.wait_for()

    def click_cart_close_btn(self):
        self.cart_drawer_clos_btn.click()

    def validate_items_in_cart(self, cart: List[dict]):
        self.validate_cart(cart, self.item_els, self.item_name, self.item_vendor, self.item_quantity, self.item_price,
                           self.item_total_price)

    def click_cart_page_btn(self):
        self.cart_page_btn.click()

    def change_cart_quantities_cart_drawer(self, cart: List[dict], amounts: [int]) -> List[dict]:
        cart = self.change_cart_quantities(self, cart, amounts, self.item_els, self.item_name, self.increase_quantity,
                                           self.decrease_quantity, self.item_quantity, self.item_error, self.cart_btn)
        return cart

    def remove_item_cart_drawer(self, item: dict, cart: List[dict]) -> List[dict]:
        cart = self.remove_item(item, cart, self.item_els, self.item_name, self.remove_button)
        return cart
