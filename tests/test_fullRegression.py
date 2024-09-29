from typing import List, Dict

from playwright.sync_api import Page

from overstock.pages.cartDrawer import CartDrawer
from overstock.pages.cartPage import CartPage
from overstock.pages.itemPage import ItemPage
from overstock.pages.homePage import HomePage
from overstock.pages.resultsPage import ResultsPage


def test_full_regression(page: Page):
    cart: List[Dict] = []
    items_quantities_add = [3, 4, 2]
    items_quantities_change = [2, -1, 6]
    remove_indexes = [0, 0]
    page.goto("https://www.overstock.com/")
    # home page
    home_page = HomePage(page)
    home_page.close_dialog()
    home_page.search_for("bracelet")
    # results page
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
        cart_drawer.check_for_discount_and_update_cart(cart)
        cart_drawer.wait_for_drawer()
        cart_drawer.validate_items_in_cart(cart)
        cart_drawer.click_cart_close_btn()
        # assert cart_count == item_page.extract_cart_num()
        new_tab.close()

    page.reload()
    home_page.click_cart()
    # validate cart page
    cart_drawer = CartDrawer(page)
    cart_drawer.click_cart_page_btn()
    cart_page = CartPage(page)
    cart_page.validate_items_in_cart(cart)
    cart_page.validate_total_price(cart)
    cart_page.page.go_back()
    home_page.click_cart()
    # change cart amounts
    cart_drawer.change_cart_quantities_cart_drawer(cart, items_quantities_change)
    cart_drawer.check_for_discount_and_update_cart(cart)
    cart_drawer.validate_items_in_cart(cart)
    # remove item cart drawer
    cart_drawer.remove_item_cart_drawer(cart[remove_indexes[0]], cart)
    cart_drawer.check_for_discount_and_update_cart(cart)
    cart_drawer.validate_items_in_cart(cart)
    cart_drawer.click_cart_page_btn()
    # remove  item cart page
    cart_page.remove_item_cart_page(cart[remove_indexes[1]], cart)
    cart_drawer.check_for_discount_and_update_cart(cart)
    cart_drawer.validate_items_in_cart(cart)
