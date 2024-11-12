import pytest
from overstock.common_page import CommonPage
from overstock.pages.cart_drawer import CartDrawer
from overstock.pages.cart_page import CartPage
from overstock.pages.home_page import HomePage
from overstock.pages.results_page import ResultsPage
from utils.utils import Utils

def test_add_and_remove_products_e2e(page, data):

    cart: list[dict[str, str | int | float]] = []
    items_quantities_add = data["items_quantities_add"]
    items_quantities_change = data["items_quantities_change"]
    remove_indexes_cart_drawer = data["remove_indexes_cart_drawer"]
    remove_indexes_cart_page = data["remove_indexes_cart_page"]
    url = data["url"]
    query = data["query"]

    page.goto(url)

    # starting at home page
    home_page = HomePage(page)
    home_page.close_dialog()
    # search bar query
    home_page.search_for(query)
    # adding items from results page
    common_page = CommonPage(page)
    common_page.add_items_from_results_page(items_quantities_add, cart)
    page.reload()
    home_page.click_cart()
    # validating cart page
    cart_drawer = CartDrawer(page)
    cart_drawer.click_cart_page_button()
    cart_page = CartPage(page)
    cart_page.validate_items_in_cart(cart)
    cart_page.validate_total_price(cart)
    # navigating to cart drawer
    cart_page.page.go_back()
    home_page.click_cart()
    # changing amounts in cart drawer
    cart_drawer.change_cart_quantities_cart_drawer(cart, items_quantities_change)
    cart_drawer.check_for_discount_and_update_cart(cart)
    # validating cart drawer
    cart_drawer.validate_items_in_cart(cart)
    # removing items in cart drawer
    cart_drawer.remove_multiple_items(cart, remove_indexes_cart_drawer)
    # navigating to cart page
    cart_drawer.click_cart_page_button()
    # removing items in cart page
    cart_page.remove_multiple_items(cart, remove_indexes_cart_page)