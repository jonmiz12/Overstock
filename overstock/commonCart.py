import time
from typing import List

from playwright.sync_api import Page, Locator

from overstock.basePage import BasePage


class CommonCart(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    def increase_item_quantity(self, item_els: Locator, item_quantity: Locator, item_error: Locator,
                               increase_quantity: Locator, cart_btn: Locator, actual_item: Locator, index: int,
                               iterator: int, remove_counter: int, cart: List[dict], amount: int) -> List[dict]:
        cart = self.validate_maximum_quantities(item_els, item_quantity, item_error, increase_quantity,
                                                cart_btn, actual_item, index, cart, amount)
        actual_amount = self.return_actual_amount(actual_item, item_quantity)
        amount = amount - 1
        item = cart[iterator - remove_counter]
        amount = self.calculate_amount_by_max_quantity(actual_amount, item, amount)
        cart_index = iterator - remove_counter
        for k in range(amount):
            actual_item.locator(increase_quantity).click()
            time.sleep(3)
            is_error = self.is_max_error_displayed(item_error)
            if is_error:
                actual_amount = self.return_actual_amount(actual_item, item_quantity)
                amount = 0
                item["max_quantity"] = actual_amount
                break
        cart[cart_index] = self.assert_quantity(actual_amount, amount, actual_item, item_quantity, item)
        return cart

    def decrease_item_quantity(self, item_els: Locator, item_quantity: Locator, item_error: Locator,
                               decrease_quantity: Locator, cart_btn: Locator, actual_item: Locator, index: int,
                               iterator: int, remove_counter: int, cart: List[dict], amount: int) -> (List[dict], int):
        if self.return_actual_amount(actual_item, item_quantity) != 1:
            # if amount * -1 > self.return_actual_amount(actual_item, item_quantity):
            cart = self.validate_maximum_quantities(item_els, item_quantity, item_error, decrease_quantity,
                                                    cart_btn, actual_item, index, cart, amount)
            amount = amount + 1
        actual_amount = self.return_actual_amount(actual_item, item_quantity)
        item = cart[iterator - remove_counter]
        amount = self.calculate_amount_by_max_quantity(actual_amount, item, amount)
        is_remove = False
        for k in range(amount * -1):
            is_remove = amount * -1 == actual_amount and k + 1 == amount * -1
            actual_item.locator(decrease_quantity).click()
            time.sleep(3)
        if is_remove:
            cart = self.validate_item_is_removed(cart[iterator - remove_counter], cart, item_els)
            remove_counter = remove_counter + 1
        else:
            cart[iterator - remove_counter] = self.assert_quantity(actual_amount, amount, actual_item,
                                                                   item_quantity,
                                                                   cart[iterator - remove_counter])
        return cart, remove_counter

    def change_cart_quantities(self, cart: List[dict], amounts: [int], item_els: Locator, item_name: Locator,
                               increase_quantity: Locator, decrease_quantity: Locator, item_quantity: Locator,
                               item_error: Locator, cart_btn: Locator) -> List[dict]:
        remove_counter = 0
        for iterator in range(len(amounts)):
            index = -1
            for actual_item in item_els.all():
                index = index + 1
                amount = amounts[(len(amounts) - iterator) - 1]
                actual_item_name = actual_item.locator(item_name).inner_text()
                if actual_item_name != cart[iterator - remove_counter]["name"]: continue
                if amount > 0:
                    cart = self.increase_item_quantity(item_els, item_quantity, item_error,
                                                       increase_quantity, cart_btn, actual_item, index,
                                                       iterator, remove_counter, cart, amount)
                elif amount < 0:
                    cart, remove_counter = self.decrease_item_quantity(item_els, item_quantity, item_error,
                                                                       decrease_quantity, cart_btn, actual_item, index,
                                                                       iterator, remove_counter, cart, amount)
                break
        return cart

    def validate_maximum_quantities(self, item_els: Locator, item_quantity: Locator, item_error: Locator,
                                    item_adjust: Locator, cart_btn: Locator, actual_item_el: Locator, item_el_index,
                                    cart: List[dict], amount: int = None) -> List[dict]:
        before_quantities = self.return_current_quantities(item_els, item_quantity)
        actual_item_el.locator(item_adjust).click()
        time.sleep(3)

        unmatched_quantities = self.create_unmatched_quantities(before_quantities, item_els, item_quantity, amount, item_el_index)
        text = None
        for item in item_els.all():
            text = item.locator(item_error).inner_text()
            if text is not '':
                break

        if not text.startswith("You can't add more") and len(unmatched_quantities) == 0:
            return cart
        else:
            self.page.reload()
            cart_btn.click()
            unmatched_quantities = self.create_unmatched_quantities(before_quantities, item_els, item_quantity, amount, item_el_index)
            if len(unmatched_quantities) != 0:
                for unmatched_quantity in unmatched_quantities:
                    cart[unmatched_quantity[0]]["max_quantity"] = unmatched_quantity[1]
        return cart

    def validate_cart(self, cart: List[dict], item_els: Locator, item_name: Locator, item_vendor: Locator, item_quantity: Locator,
                      item_price: Locator, item_total_price: Locator):
        actual_items_count = item_els.count()
        assert len(cart) == actual_items_count, f"len(cart): {len(cart)}, actual_items_count: {actual_items_count} for cart '{cart}'"
        for index in range(actual_items_count):
            item_failed_assertions = []
            actual_item_name = item_name.nth(index).inner_text()
            actual_vendor = item_vendor.nth(index).inner_text()
            actual_item_price = self.custom_round(float(self.extract_clean_text(item_price.nth(index).inner_text(), "$", True)))
            actual_item_total_price = round(
                float(self.extract_clean_text(item_total_price.nth(index).inner_text(), "$", True)), 0)
            actual_item_quantity = float(item_els.nth(index).locator(item_quantity).get_attribute("value"))

            item = next((item for item in cart if item['name'] == actual_item_name), None)

            if not item:
                raise AssertionError(f"Item '{actual_item_name}' not found in cart.\nThe cart: {cart}")
            expected_price = self.custom_round(float(item["raw_price"]))
            expected_quantity = float(item["quantity"])
            expected_total_price = round(item['raw_price'] * expected_quantity, 0)
            expected_vendor = item['vendor']

            if expected_quantity != actual_item_quantity:
                item_failed_assertions.append(f"expected_quantity: {expected_quantity}, actual_quantity {actual_item_quantity}\nfor item: {item},\n in cart: {cart}\n")
            if expected_price != actual_item_price:
                item_failed_assertions.append(f"expected_price: {expected_price}, actual_item_price {actual_item_price}\nfor item: {item},\n in cart: {cart}\n")
            if expected_total_price != actual_item_total_price:
                item_failed_assertions.append(f"expected_total_price: {expected_total_price}, actual_total_price {actual_item_total_price}\nfor item: {item},\n in cart: {cart}\n")
            if expected_vendor != actual_vendor:
                item_failed_assertions.append(f"expected_vendor: {expected_vendor}, actual_vendor {actual_vendor}\nfor item: {item},\n in cart: {cart}\n")
            for item_error in item_failed_assertions:
                self.add_failed_assertion(item_error)
                self.get_screenshot()
