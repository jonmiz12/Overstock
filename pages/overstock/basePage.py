from typing import List, Dict

from playwright.sync_api import Page, Locator

discount = 1


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def create_item(self, cart: List, item_name: str, raw_price: float, total_price: int = 0, quantity: int = 0,
                    properties: Dict = None) -> List:
        item = {
            'name': item_name,
            'original_price': float(raw_price),
            'price': round(float(raw_price), 1),
            'total_price': total_price,
            'quantity': quantity,
            'properties': properties,
            'raw_price': raw_price
        }
        item = self.adjust_price_to_discount(item)
        cart.append(item)
        return cart

    @staticmethod
    def update_quantity(cart: [], quantity: int, item_name: str):
        for item in cart:
            if item['name'] == item_name:
                item['quantity'] = quantity
                break

    @staticmethod
    def return_clean_text(text: str, indicator: str, remove_indicator: bool = False) -> str:
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
        global discount
        total = 0
        for item in cart:
            price = item['original_price'] * float(item["quantity"])
            total = round(total + price, 2)
        if total < 750 and discount == 1:
            None
        elif total < 1000 and discount != 0.85:
            for item in cart:
                item = self.adjust_price_to_discount(item)
            discount = 0.85
        elif total >= 1000 and discount != 0.80:
            discount = 0.80
            for item in cart:
                item = self.adjust_price_to_discount(item)
            discount = 0.80
        return cart

    @staticmethod
    def adjust_price_to_discount(item: [dict]):
        global discount
        price = float(round(item['raw_price'] * discount, 1))
        item['price'] = round(price, 1)
        item['raw_price'] = round(item['raw_price'] * discount, 2)
        return item

    def validate_cart(self, cart: List[dict], item_els: Locator, item_name: Locator, item_quantity: Locator,
                      item_price: Locator, item_total_price: Locator):
        actual_items_count = item_els.count()
        assert len(cart) == actual_items_count, f"len(cart): {len(cart)}, actual_items_count {actual_items_count} for item '{cart}'"

        for index in range(actual_items_count):
            actual_item_name = item_name.nth(index).inner_text()
            actual_item_price = round(float(self.return_clean_text(item_price.nth(index).inner_text(), "$", True)), 1)
            actual_item_total_price = round(
                float(self.return_clean_text(item_total_price.nth(index).inner_text(), "$", True)), 1)
            actual_item_quantity = float(item_quantity.nth(index).get_attribute("value"))

            item = next((item for item in cart if item['name'] == actual_item_name), None)

            if not item:
                raise AssertionError(f"Item '{actual_item_name}' not found in cart")

            expected_price = float(item["price"])
            expected_quantity = float(item["quantity"])
            expected_total_price = round(item['raw_price'] * expected_quantity, 1)

            assert expected_quantity == actual_item_quantity, f"expected_quantity: {expected_quantity}, actual_quantity {actual_item_quantity} for item '{item}'"
            assert expected_price == actual_item_price, f"expected_price: {expected_price}, actual_item_price {actual_item_price} for item '{item}'"
            assert expected_total_price == actual_item_total_price, f"expected_total_price: {expected_total_price}, actual_total_price {actual_item_total_price} for item '{item}'"
