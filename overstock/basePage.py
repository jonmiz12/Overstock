import logging
import math
import time
import os
from typing import List, Dict

from colorama import Fore, Style

from utils import utils
from utils.utils import Utils

from playwright.sync_api import Page, Locator

DISCOUNT = 1
DISCOUNT_THRESHOLD = 1000


class CustomError(Exception):
    pass


class BasePage:
    failed_assertions = []

    def __init__(self, page: Page):
        self.page = page

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

    @staticmethod
    def update_quantity(cart: [], quantity: int, item_name: str):
        for item in cart:
            if item['name'] == item_name:
                item['quantity'] = quantity
                break

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

    @staticmethod
    def apply_discount_to_item(item: [dict]):
        global DISCOUNT
        price = float(round(item['original_price'] * DISCOUNT, 1))
        item['price'] = round(price, 1)
        item['raw_price'] = item['original_price'] * DISCOUNT
        return item

    @staticmethod
    def return_current_quantities(item_els: Locator, item_quantity: Locator) -> [int]:
        quantities = []
        for item in item_els.all():
            quantity = int(item.locator(item_quantity).get_attribute("value"))
            quantities.append(quantity)
        return quantities

    @staticmethod
    def sign(amount: int) -> int:
        return 1 if amount > 0 else -1

    def create_unmatched_quantities(self, before_quantities: [], item_els: Locator, item_quantity: Locator, amount: int,
                                    item_el_index=None) -> []:
        quantities_len = len(before_quantities)
        after_quantities = self.return_current_quantities(item_els, item_quantity)
        unmatched_quantities = []
        pos_or_neg = self.sign(amount)
        for index in range(quantities_len - 1, -1, -1):
            if before_quantities[index] != after_quantities[index]:
                unmatched = [index, after_quantities[index]]
                temp = before_quantities[index] + pos_or_neg == unmatched[1]
                if unmatched[0] == item_el_index and temp:
                    continue
                unmatched_quantities.append(unmatched)
        return unmatched_quantities

    def adjust_cart_to_quantities(self, cart: List[dict], item_els: Locator, item_quantity: Locator) -> List[dict]:
        quantities = self.return_current_quantities(item_els, item_quantity)
        for iterator in range(len(cart)):
            cart[iterator]["quantity"] = quantities[len(quantities) - 2 - iterator]
        return cart

    @staticmethod
    def raise_max_quantity_error():
        try:
            raise CustomError(f"Max quantity reached! Bypassing test data with default max quantities")
        except CustomError as e:
            logging.error(f"Error occurred: {e}")

    def remove_item(self, item: dict, cart: List[dict], item_els: Locator, item_name: Locator,
                    remove_button: Locator) -> List[dict]:
        for item_el in item_els.all():
            if item_el.locator(item_name).inner_text() != item["name"]:
                continue
            item_el.locator(remove_button).click()
            time.sleep(3)
            break
        cart = self.validate_item_is_removed(item, cart, item_els, item_name)
        return cart

    def validate_item_is_removed(self, removed_item: [dict], cart: List[dict], item_els: Locator, item_name: Locator) -> \
            List[dict]:
        actual_item_count = item_els.count()
        expected_item_count = len(cart) - 1

        if expected_item_count != actual_item_count:
            self.get_screenshot()
            self.add_failed_assertion(f"len(cart) - 1: {len(cart) - 1}, actual_item_count: {actual_item_count}")

        match = False
        for item_el in item_els.all():
            actual_item_name = item_el.locator(item_name).inner_text()
            if actual_item_name == removed_item["name"]: continue
            match = True

        if not match:
            self.get_screenshot()
            assert False, f"expected to remove item: {removed_item['name']}.\nfrom cart: {cart}"

        cart.remove(removed_item)
        return cart

    @staticmethod
    def return_actual_amount(item_el: Locator, item_quantity: Locator) -> int:
        amount = int(item_el.locator(item_quantity).get_attribute("value"))
        return amount

    def assert_quantity(self, initial_amount: int, amount: int, item_el: Locator, item_quantity: Locator,
                        item: dict) -> dict:
        result_amount = initial_amount + amount
        actual_amount = self.return_actual_amount(item_el, item_quantity)
        if result_amount != actual_amount:
            self.get_screenshot()
            self.add_failed_assertion(
                f"result_amount: {result_amount}, actual_amount: {actual_amount} for item '{item}'")
        item["quantity"] = result_amount
        return item

    @staticmethod
    def calculate_amount_by_max_quantity(actual_amount: int, item: dict, amount: int) -> int:
        expected_final_amount = actual_amount + amount
        item_max_quantity = item["max_quantity"] or 0
        if expected_final_amount > item_max_quantity and item_max_quantity is not 0:
            return item_max_quantity - actual_amount
        elif expected_final_amount < 0:
            return actual_amount * -1
        else:
            return amount

    @staticmethod
    def is_max_error_displayed(item_error: Locator) -> bool:
        is_error_displayed = False
        for item_error in item_error.all():
            if item_error.inner_text().startswith("You can't add more"):
                is_error_displayed = True
                break
        return is_error_displayed

    @staticmethod
    def custom_round(number: float) -> float:
        rounded = math.ceil(number * 2) / 2
        return round(rounded, 2)

    @staticmethod
    def round_down_on_half(number: float) -> float:
        if number % 1 == 0.5:
            return float(math.floor(number))
        else:
            return round(number)

    def get_screenshot(self):
        # dire = "C:\\Users\\jonmi\\PycharmProjects\\playwrightPy\\tempPic"
        # self.page.screenshot(path=f'{dire}.png')
        # assert False
        current_datetime = Utils.get_current_datetime()
        screenshot_path = Utils.TEST_REPORT_DIR + "\\" + Utils.START_TIME + "\\" + current_datetime
        # print(f"THIS IS WHERE THE SCREENSHOT HAPPENS - {screenshot_path}")
        # print("")
        # print("")
        # print("")
        self.page.screenshot(path=f"{screenshot_path}.png", full_page=True)

    @classmethod
    def add_failed_assertion(cls, error):
        current_datetime = Utils.get_current_datetime()
        if isinstance(cls.failed_assertions, list):
            cls.failed_assertions.append(error + " " + current_datetime)
        else:
            print("Error: self.errors is not a list.")

    @classmethod
    def print_failed_assertions(cls) -> []:
        for failed_assertion in cls.failed_assertions:
            print(Fore.RED + f"{failed_assertion}" + Style.RESET_ALL + "\n")
        assert len(cls.failed_assertions) == 0

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
                    log_file.write(f"{failed_assertion}\n")
            else:
                log_file.write("No product errors.\n")
            # Checking for non-assertion errors
            rep_call = getattr(request.node, "rep_call", None)  # Test execution result
            if rep_call and rep_call.failed:
                log_file.write(f"\nTest defect error:\n{rep_call.longreprtext}\n")
            else:
                log_file.write("No test defect errors.\n")

        print(Fore.GREEN + f"\nLog file created at: {log_file_path}" + Style.RESET_ALL)

    def assert_responses(self, responses: [], valid_responses: []):
        failed_responses = []
        for response in responses:
            status: str = response.status
            if not valid_responses.__contains__(status):
                failed_responses.append(response)

        for failed_response in failed_responses:
            self.add_failed_assertion(f"Found invalid response status: {failed_response}")
        # Asserts no failed responses found
        # assert len(failed_responses) == 0, f"failed responses: {failed_responses}"