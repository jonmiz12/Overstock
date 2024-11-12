from overstock.common_page import CommonPage
from overstock.pages.cart_drawer import CartDrawer
from overstock.pages.cart_page import CartPage
from overstock.pages.home_page import HomePage

def test_add_from_item_page_e2e(page, data):

    cart: list[dict[str, str | int | float]] = []
    items_quantities_add = data["items_quantities_add"]
    url = data["url"]
    query = data["query"]

    page.goto(url)

    # starting at home page
    home_page = HomePage(page)
    home_page.close_dialog()
    # search bar query
    home_page.search_for(query)
    # clicking items in results page and adding them from item page
    common_page = CommonPage(page)
    common_page.add_items_from_results_page(items_quantities_add, cart)

def test_add_from_cart_page_e2e(page, data):

    cart: list[dict[str, str | int | float]] = []
    items_quantities_add = data["items_quantities_add"]
    items_quantities_change = data["items_quantities_change"]
    url = data["url"]
    query = data["query"]

    page.goto(url)

    # starting at home page
    home_page = HomePage(page)
    home_page.close_dialog()
    # search bar query
    home_page.search_for(query)
    # clicking items in results page and adding them from item page
    common_page = CommonPage(page)
    common_page.add_items_from_results_page(items_quantities_add, cart)
    # navigating to cart page
    cart_drawer = CartDrawer(page)
    page.reload()
    home_page.click_cart()
    cart_drawer.click_cart_page_button()
    # adding items from cart page
    cart_page = CartPage(page)
    cart_page.change_cart_quantities_cart_page(cart, items_quantities_change)
    cart_drawer.check_for_discount_and_update_cart(cart)
    cart_drawer.validate_items_in_cart(cart)

def test_add_from_cart_drawer_e2e(page, data):

    cart: list[dict[str, str | int | float]] = []
    items_quantities_add = data["items_quantities_add"]
    items_quantities_change = data["items_quantities_change"]
    url = data["url"]
    query = data["query"]

    page.goto(url)

    # starting at home page
    home_page = HomePage(page)
    home_page.close_dialog()
    # search bar query
    home_page.search_for(query)
    # clicking items in results page and adding them from item page
    common_page = CommonPage(page)
    common_page.add_items_from_results_page(items_quantities_add, cart)
    # navigating to cart page
    page.reload()
    home_page.click_cart()
    # adding items from cart drawer
    cart_drawer = CartDrawer(page)
    cart_drawer.change_cart_quantities_cart_drawer(cart, items_quantities_change)
    cart_drawer.check_for_discount_and_update_cart(cart)
    cart_drawer.validate_items_in_cart(cart)