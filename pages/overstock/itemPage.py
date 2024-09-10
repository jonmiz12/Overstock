import time
from typing import List

from playwright.sync_api import Page, expect
from pages.overstock.header import Header

discount_state = 0


class ItemPage(Header):

    def __init__(self, page: Page):
        super().__init__(page)
        global discount_state
        self.discount_state = discount_state
        self.page = page
        self.add_to_cart_btn = page.locator(".product-info__add-button [type='submit']")
        self.options_elements = page.locator(".custom-select")
        self.options_options = page.locator('ul>li')
        self.item_name = page.locator(".product-title")
        self.item_price = page.locator(".product-info__price .price__current strong")
        self.item_quantity = page.locator("[id^='quantity-template']")
        self.increase_quantity = page.locator(".product-info__sticky [name='plus']")
        self.decrease_quantity = page.locator(".product-info__sticky [name='minus']")

    def click_add_to_cart(self):
        self.add_to_cart_btn.click()

    # def fill_selects(self):

    def find_option_price(self, price: str):
        match = False
        actual_price = round(float(self.return_clean_text(self.item_price.inner_text(), "$", True)), 1)
        if price == actual_price: match = True
        select_count = self.options_elements.count()
        for option_header in self.options_elements.all():
            if match: break
            for option in option_header.locator(self.options_options).all():
                option_header.click()
                option.click()
                actual_price = self.return_clean_text(self.item_price.inner_text(), "$")
                if actual_price == price:
                    match = True
                    break

    def extract_item_name(self) -> str:
        return self.item_name.inner_text()

    def validate_item_name_price(self, cart: List[dict]):
        match = False
        time.sleep(2)
        actual_name = self.item_name.inner_text()
        for item in cart:
            if item["name"] != actual_name: continue
            match = True
            self.find_option_price(item["price"])
            price = round(float(self.return_clean_text(self.item_price.inner_text(), "$", True)), 1)
            assert (round(item["original_price"], 1) == price), f""
            break
        assert match, f"couldn't find the actual_name: {actual_name}, in the cart: {cart}"

    def change_amount(self, amount: int, cart: List[dict]) -> List[dict]:
        amount = amount - 1
        if amount > 0:
            for iterator in range(amount):
                self.increase_quantity.click()
                self.item_quantity.wait_for()
        return cart

    def change_quantity_add_to_cart(self, amount: int, cart: List[dict]) -> List[dict]:
        cart = self.change_amount(amount, cart)
        cart = self.update_item_quantity(cart, str(amount))
        cart = self.check_for_discount_and_update_cart(cart)
        self.add_to_cart_btn.click()
        return cart

    def update_item_quantity(self, cart: List[dict], amount: str) -> List[dict]:
        item_name = self.item_name.inner_text()
        item = next((item for item in cart if item['name'] == item_name), None)
        if item:
            item['quantity'] = amount
            return cart
        else:
            raise ValueError(f"Item '{item_name}' not found in cart")
