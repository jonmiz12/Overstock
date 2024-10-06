import inspect
import math
import os
from pathlib import Path
from typing import List, Dict

import allure
from colorama import Fore, Style

from utils.utils import Utils

from playwright.sync_api import Page, Locator

DISCOUNT = 1
DISCOUNT_THRESHOLD = 1000


class BasePage:
    failed_assertions = []

    def __init__(self, page: Page):
        # Initializes the BasePage class with a Playwright page object.
        self.page = page

    # Creates an item with the given data and adds it to the cart. Applies a discount before inserting the item at the beginning of the cart.
    def create_item(self, cart: List, item_data: dict, total_price: int = 0, quantity: int = 0,
                    properties: Dict = None, max_quantity: float = None) -> List:
        item = {
            'name': item_data["name"],
            'original_price': float(item_data["raw_price"]),
            'price': round(float(item_data["raw_price"]), 1),
            'total_price': total_price,
            'quantity': quantity,
            'properties': properties,
            'raw_price': item_data["raw_price"],
            'max_quantity': max_quantity,
            'vendor': item_data["vendor"]
        }
        item = self.apply_discount_to_item(item)
        cart.insert(0, item)
        return cart

    # Updates the quantity of a specific item in the cart by matching its name.
    @staticmethod
    def update_quantity(cart: [], quantity: int, item_name: str):
        for item in cart:
            if item['name'] == item_name:
                item['quantity'] = quantity
                break

    # Removes commas from text and extracts part of the text based on the given indicator. Optionally, the indicator can be removed from the result.
    @staticmethod
    def extract_clean_text(text: str, indicator: str, remove_indicator: bool = False) -> str:
        text = text.replace(",", "")
        index = text.find(indicator)
        if index != -1:
            if not remove_indicator:
                return text[index:]
            elif remove_indicator:
                return text[index + 1:]
        else:
            return ""

    # Checks the total price of the cart, determines if a discount is applicable, and applies the discount to all items in the cart.
    # The site changes the discount rules from time to time so the commented out rule can be added at any time.
    def check_for_discount_and_update_cart(self, cart: List[dict]) -> List[dict]:
        global DISCOUNT
        total = 0
        for item in cart:
            price = item['original_price'] * float(item["quantity"])
            total = total + price
        if total < DISCOUNT_THRESHOLD:
            DISCOUNT = 1
            for item in cart:
                item = self.apply_discount_to_item(item)
        # elif total < 1000:
        #     discount = 0.85
        #     for item in cart:
        #         item = self.adjust_price_to_discount(item)
        elif total >= DISCOUNT_THRESHOLD:
            DISCOUNT = 0.85
            for item in cart:
                item = self.apply_discount_to_item(item)
        return cart

    # Applies the global discount to an item's price and updates its 'raw_price' and 'price' fields.
    @staticmethod
    def apply_discount_to_item(item: [dict]):
        global DISCOUNT
        price = float(round(item['original_price'] * DISCOUNT, 1))
        item['price'] = round(price, 1)
        item['raw_price'] = item['original_price'] * DISCOUNT
        return item

    # Returns the current quantities of all items based on their locator and the item_quantity element.
    @staticmethod
    def return_current_quantities(item_els: Locator, item_quantity: Locator) -> [int]:
        quantities = []
        for item in item_els.all():
            quantity = int(item.locator(item_quantity).get_attribute("value"))
            quantities.append(quantity)
        return quantities

    # Returns 1 if the amount is positive, otherwise returns -1.
    @staticmethod
    def sign(amount: int) -> int:
        return 1 if amount > 0 else -1

    # Adjusts the cart to match the current quantities of items based on locators.
    def adjust_cart_to_quantities(self, cart: List[dict], item_els: Locator, item_quantity: Locator) -> List[dict]:
        quantities = self.return_current_quantities(item_els, item_quantity)
        for iterator in range(len(cart)):
            cart[iterator]["quantity"] = quantities[len(quantities) - 2 - iterator]
        return cart

    # Returns the current amount (quantity) of a specific item.
    @staticmethod
    def return_actual_amount(item_el: Locator, item_quantity: Locator) -> int:
        amount = int(item_el.locator(item_quantity).get_attribute("value"))
        return amount

    # Calculates the amount to be adjusted based on the maximum quantity allowed for an item.
    @staticmethod
    def calculate_amount_by_max_quantity(actual_amount: int, item: dict, amount: int) -> int:
        expected_final_amount = actual_amount + amount
        item_max_quantity = item["max_quantity"] or 0
        if expected_final_amount > item_max_quantity != 0:
            return item_max_quantity - actual_amount
        elif expected_final_amount < 0:
            return actual_amount * -1
        else:
            return amount

    # Checks if the "max quantity" error message is displayed for any item in the cart.
    @staticmethod
    def is_max_error_displayed(item_error: Locator) -> bool:
        is_error_displayed = False
        for item_error in item_error.all():
            if item_error.inner_text().startswith("You can't add more"):
                is_error_displayed = True
                break
        return is_error_displayed

    # Rounds the given number to the nearest half (0.5 increments).
    @staticmethod
    def custom_round(number: float) -> float:
        rounded = math.ceil(number * 2) / 2
        return round(rounded, 2)

    # Rounds down the number if it ends in 0.5, otherwise rounds it normally.
    @staticmethod
    def round_down_on_half(number: float) -> float:
        if number % 1 == 0.5:
            return float(math.floor(number))
        else:
            return round(number)

    # Takes a full-page screenshot and saves it to a specified path or the default test report folder, either using
    # 'self.page' or the provided 'page'.
    def get_screenshot_in_test_report(self=None, page: Page = None, file_name=None):
        if self:
            page = self.page
        elif page is None:
            raise ValueError("A valid 'page' object must be provided when calling this method without 'self'.")
        if file_name is None:
            file_name = Utils.get_current_datetime()
        screenshot_path = Utils.TEST_REPORT_DIR + "\\" + Utils.START_TIME + "\\" + file_name
        page.screenshot(path=f"{screenshot_path}.png", full_page=True)
        print(Fore.GREEN + f"\nSaved screenshot at: {screenshot_path}" + Style.RESET_ALL)

    # Adds an error message with the name of the method from an inspect object and timestamp to the 'failed_assertions' list.
    @classmethod
    def add_failed_assertion(cls, error, method_name):
        current_datetime = Utils.get_current_datetime()
        if isinstance(cls.failed_assertions, list):
            cls.failed_assertions.append("Method name: " + method_name + "\n" + error + "\n" + current_datetime)
        else:
            print("Error: self.errors is not a list.")

    # Prints all failed assertions in red text. If any failed assertions exist, it will raise an assertion error.
    @classmethod
    def print_failed_assertions(cls) -> []:
        for failed_assertion in cls.failed_assertions:
            print(Fore.RED + f"{failed_assertion}" + Style.RESET_ALL + "\n")
        assert len(cls.failed_assertions) == 0

    # Creates a log file for the test, recording any failed assertions and test defects. The log file is saved in a directory
    # based on the current test's start time and name. If there are no product errors or test defect errors, the log will indicate that.
    @classmethod
    def create_logfile(cls, request):
        start_time = Utils.START_TIME
        path = Utils.TEST_REPORT_DIR
        test_name = request.node.originalname
        log_file_path = os.path.join(path, start_time, test_name + ".log")
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            if cls.failed_assertions:
                log_file.write(f"Product errors:\n")
                for failed_assertion in cls.failed_assertions:
                    log_file.write(f"\n{failed_assertion}\n")
            else:
                log_file.write("\nNo product errors.\n")
            rep_call = getattr(request.node, "rep_call", None)
            if rep_call and rep_call.failed:
                log_file.write(f"\nTest defect error: \n{rep_call.longreprtext}\n")
            else:
                log_file.write("\nNo test defect errors.\n")
        print(Fore.GREEN + f"\nLog file created at: {log_file_path}" + Style.RESET_ALL)

    # Compares a list of responses against valid responses, and adds any invalid response statuses to the failed
    # assertions list.
    def assert_responses(self, responses: [], valid_responses: []):
        failed_responses = []
        for response in responses:
            status: str = response.status
            if not valid_responses.__contains__(status):
                failed_responses.append(response)
        for failed_response in failed_responses:
            self.add_failed_assertion(f"Found invalid response status: {failed_response}", inspect.currentframe().f_code.co_name)

    # Attach the screenshots and logs for a given test to the Allure report.
    @staticmethod
    def attach_test_artifacts():
        folder = Path(f"{Utils.TEST_REPORT_DIR}/{Utils.START_TIME}")

        # Attach screenshots
        for screenshot_file in folder.glob("*.png"):
            with open(screenshot_file, "rb") as screenshot:
                allure.attach(screenshot.read(), name=screenshot_file.name, attachment_type=allure.attachment_type.PNG)

        # Attach logs
        for log_file in folder.glob("*.log"):
            with open(log_file, "r") as log:
                allure.attach(log.read(), name=log_file.name, attachment_type=allure.attachment_type.TEXT)
