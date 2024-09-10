from typing import List, Dict

from playwright.sync_api import Page

from pages.overstock.cartDrawer import CartDrawer
from pages.overstock.cartPage import CartPage
from pages.overstock.itemPage import ItemPage
from pages.overstock.homePage import HomePage
from pages.overstock.resultsPage import ResultsPage


def test_add_items_to_cart(page: Page):
    cart: List[Dict] = []
    items_quantities = [2, 1, 4, 3, 5, 1, 1]
    page.goto("https://www.overstock.com/")

    # home page
    home_page = HomePage(page)
    home_page.close_dialog()
    home_page.search_for("bracelet")
    # results page
    results_page = ResultsPage(page)
    for iterator in range(len(items_quantities)):
        data = results_page.return_item_data(iterator)
        cart = results_page.create_item(cart, data['name'], data['raw_price'])
        results_page.click_item(iterator)
        new_tab = page.context.wait_for_event('page')
        new_tab.wait_for_load_state()
        # item page
        item_page = ItemPage(new_tab)
        item_page.validate_item_name_price(cart)
        # item_page.fill_selects()
        cart = item_page.change_quantity_add_to_cart(items_quantities[iterator], cart)
        cart_drawer = CartDrawer(new_tab)
        cart_drawer.wait_for_drawer()
        cart_drawer.validate_items_in_cart(cart)
        cart_drawer.click_cart_close_btn()
        # assert cart_count == item_page.extract_cart_num()
        new_tab.close()

    page.reload()
    home_page.click_cart()
    cart_drawer = CartDrawer(page)
    cart_drawer.click_cart_page_btn()
    cart_page = CartPage(page)
    cart_page.validate_items_in_cart(cart)
    cart_page.validate_total_price(cart)

