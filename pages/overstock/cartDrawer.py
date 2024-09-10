import time
from typing import List

from playwright.sync_api import Page, expect
from pages.overstock.header import Header


class CartDrawer(Header):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.drawer_el = page.locator("cart-drawer.drawer")
        self.item_els = page.locator(".cart-items tbody>tr")
        self.item_name = page.locator(".cart-item__title")
        self.item_price = page.locator(".cart-item__info .price__current")
        self.item_total_price = page.locator(".cart-item__total .price__current")
        self.item_quantity = page.locator(".cart-items [id^='quantity']")
        self.cart_drawer_clos_btn = page.locator(".drawer__close-btn")
        self.cart_page_btn = page.locator(".cart-drawer__view-cart")

    @staticmethod
    def wait_for_drawer():
        # while True:
        #     try:
        #         text = self.item_els.inner_text()
        #         if text != "":
        #             break
        #     except:
        #         continue
        time.sleep(4)

    def click_cart_close_btn(self):
        self.cart_drawer_clos_btn.click()

    def validate_items_in_cart(self, cart: List[dict]):
        self.validate_cart(cart, self.item_els, self.item_name, self.item_quantity, self.item_price, self.item_total_price)

    def click_cart_page_btn(self):
        self.cart_page_btn.click()
