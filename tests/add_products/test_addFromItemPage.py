from typing import List, Dict

from playwright.sync_api import Page

from overstock.pages.cartDrawer import CartDrawer
from overstock.pages.itemPage import ItemPage
from overstock.pages.homePage import HomePage
from overstock.pages.resultsPage import ResultsPage


def test_add_from_item_page(page: Page):
    cart: List[Dict] = []
    items_quantities_add = [4, 1, 4]
    page.goto("https://www.overstock.com/")

    # home page
    home_page = HomePage(page)
    home_page.close_dialog()
    home_page.search_for("bracelet")
    results_page = ResultsPage(page)
    for iterator in range(len(items_quantities_add)):
        item_data = results_page.return_item_data(iterator)
        results_page.create_item(cart, item_data)
        results_page.click_item(iterator)
        new_tab = page.context.wait_for_event('page')
        new_tab.wait_for_load_state()
        # item page
        item_page = ItemPage(new_tab)
        item_page.validate_item_data(cart)
        # item_page.fill_selects()
        cart = item_page.change_quantity_add_to_cart(items_quantities_add[iterator], cart)
        cart_drawer = CartDrawer(new_tab)
        cart_drawer.wait_for_drawer()
        cart_drawer.validate_items_in_cart(cart)
        cart_drawer.click_cart_close_btn()
        # assert cart_count == item_page.extract_cart_num()
        new_tab.close()

