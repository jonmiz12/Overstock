import inspect
from typing import List

from playwright.sync_api import Page
from overstock.pages.header import Header


class ItemPage(Header):

    def __init__(self, page: Page):
        # Initializes the ItemPage with locators for various elements on the item page (e.g., add to cart button, item name, price, quantity, etc.)
        super().__init__(page)
        self.page = page
        self.add_to_cart_btn = page.locator(".product-info__add-button [type='submit']")
        self.options_elements = page.locator(".custom-select")
        self.options_options = page.locator('ul>li')
        self.item_name = page.locator(".product-title")
        self.item_price = page.locator(".product-info__price .price__current strong:not([class='price__current'])")
        self.item_quantity = page.locator("[id^='quantity-template']")
        self.increase_quantity = page.locator(".product-info__sticky [name='plus']")
        self.decrease_quantity = page.locator(".product-info__sticky [name='minus']")
        self.item_vendor = page.locator(".product-vendor")

    # Simulates a click on the 'Add to Cart' button.
    def click_add_to_cart(self):
        self.add_to_cart_btn.click()

    # Finds the matching price by selecting various options from the dropdown, and compares the displayed price with the expected price.
    # Asserts false if no match is found
    def find_option_price(self, price: str):
        match = False
        actual_price = self.extract_clean_text(self.item_price.inner_text(), "$", True)
        # self.add_failed_assertion(f"initial price: {actual_price}. expected price: {price}", inspect.currentframe().f_code.co_name)
        price = str(price)
        if price == actual_price: match = True
        for option_header in self.options_elements.all():
            if match: break
            for option in option_header.locator(self.options_options).all():
                option_header.click()
                option.click()
                actual_price = self.extract_clean_text(self.item_price.inner_text(), "$", True)
                # self.add_failed_assertion(f"next price: {actual_price}. expected price: {price}", inspect.currentframe().f_code.co_name)
                if actual_price == price:
                    match = True
                    break
        if not match:
            self.get_screenshot_in_test_report()
            self.add_failed_assertion(f"could not find a matching price to the price in the cart", inspect.currentframe().f_code.co_name)

    # Extracts and returns the name of the item displayed on the page.
    def extract_item_name(self) -> str:
        return self.item_name.inner_text()

    # Validates that the item's name, vendor, and price match the details stored in the cart.
    # If any discrepancies are found, they are logged as failed assertions and screenshots are captured.
    def validate_item_data(self, cart: List[dict]):
        failed_assertions = []
        actual_name = self.item_name.inner_text()
        actual_vendor = self.item_vendor.inner_text()
        item = next((item for item in cart if item['name'] == actual_name), None)
        if item:
            self.find_option_price(item["original_price"])
            actual_price = round(float(self.extract_clean_text(self.item_price.inner_text(), "$", True)), 1)
            cart_original_price = round(item["original_price"], 1)
            cart_vendor = item['vendor']
            if cart_original_price != actual_price:
                failed_assertions.append(f"cart_original_price:{cart_original_price} actual price: {actual_price}")
            if cart_vendor != actual_vendor:
                failed_assertions.append(f"cart vendor:{cart_vendor} actual vendor: {actual_vendor}")
        else:
            self.get_screenshot_in_test_report()
            self.add_failed_assertion(f"No match was found for the item name: {item['name']}", inspect.currentframe().f_code.co_name)
        for failed_assertion in failed_assertions:
            self.get_screenshot_in_test_report()
            self.add_failed_assertion(failed_assertion, inspect.currentframe().f_code.co_name)

    # Increases the quantity of the item by clicking the 'plus' button based on the specified amount.
    def change_amount(self, amount: int, cart: List[dict]) -> List[dict]:
        if amount > 1:
            amount = amount - 1
            for iterator in range(amount):
                self.increase_quantity.click()
                self.item_quantity.wait_for()
        return cart

    # Changes the item quantity, updates the cart, checks for discounts, and adds the item to the cart.
    def change_quantity_add_to_cart(self, amount: int, cart: List[dict]) -> List[dict]:
        cart = self.change_amount(amount, cart)
        cart = self.update_item_quantity(cart, str(amount))
        cart = self.check_for_discount_and_update_cart(cart)
        self.add_to_cart_btn.click()
        return cart

    # Updates the item quantity in the cart. If the item is found in the cart, its quantity is updated.
    # Raises an error if the item is not found in the cart.
    def update_item_quantity(self, cart: List[dict], amount: str) -> List[dict]:
        item_name = self.item_name.inner_text()
        item = next((item for item in cart if item['name'] == item_name), None)
        if item:
            item['quantity'] = amount
            return cart
        else:
            self.get_screenshot_in_test_report()
            self.add_failed_assertion(f"Item '{item_name}' not found in cart", inspect.currentframe().f_code.co_name)
