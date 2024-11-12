import inspect
import time

from playwright.sync_api import Page, Locator

from overstock.base_page import BasePage
from overstock.pages.cart_drawer import CartDrawer
from overstock.pages.item_page import ItemPage
from overstock.pages.results_page import ResultsPage


# This class contains methods that utilizes instances of multiple pages
class CommonPage(BasePage):

    # Initializes the CommonCart class by calling the parent BasePage constructor, passing the Playwright page object.
    def __init__(self, page: Page):
        self.page = page
        self.results_page = ResultsPage(page)
        self.item_page = ItemPage(page)
        super().__init__(page)

    def add_items_from_results_page(self, items_quantities_add: [str], cart):
        for iterator in range(len(items_quantities_add)):
            item_data = self.results_page.return_item_data(iterator)
            self.results_page.create_item(cart, item_data)
            self.results_page.close_dialog()
            self.results_page.click_item(iterator)
            new_tab = self.page.context.wait_for_event('page')
            new_tab.wait_for_load_state()
            # item page
            self.item_page = ItemPage(new_tab)
            self.item_page.validate_item_data(cart)
            cart = self.item_page.change_quantity_add_to_cart(items_quantities_add[iterator], cart)
            cart_drawer = CartDrawer(new_tab)
            cart_drawer.close_dialog()
            cart_drawer.wait_for_drawer()
            cart_drawer.validate_items_in_cart(cart)
            cart_drawer.click_cart_close_button()
            new_tab.close()