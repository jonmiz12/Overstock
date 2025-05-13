from overstock.common_page import CommonPage
from overstock.pages.cart_drawer import CartDrawer
from overstock.pages.cart_page import CartPage
from overstock.pages.home_page import HomePage

def test_remove_from_cart_page_minus_e2e(page, data):

    cart: list[dict[str, str | int | float]] = []
    items_quantities_add = data["items_quantities_add"]
    items_quantities_change = data["items_quantities_change"]
    url = data["url"]
    query = data["query"]

    page.goto(url)

    # home page
    home_page = HomePage(page)
    home_page.close_dialog()
    home_page.search_for(query)
    # clicking items in results page and adding them from item page
    common_page = CommonPage(page)
    common_page.add_items_from_results_page(items_quantities_add, cart)
    # navigating to cart page
    page.reload()
    home_page.click_cart()
    cart_drawer = CartDrawer(page)
    cart_drawer.click_cart_page_button()
    # decrease items in cart page
    cart_page = CartPage(page)
    cart_page.change_cart_quantities_cart_page(cart, items_quantities_change)
    cart_drawer.check_for_discount_and_update_cart(cart)
    cart_drawer.validate_items_in_cart(cart)

def test_remove_from_cart_page_delete_e2e(page, data):

    cart: list[dict[str, str | int | float]] = []
    items_quantities_add = data["items_quantities_add"]
    remove_indexes = data["remove_indexes"]
    url = data["url"]
    query = data["query"]

    page.goto(url)

    # home page
    home_page = HomePage(page)
    home_page.close_dialog()
    home_page.search_for(query)
    # clicking items in results page and adding them from item page
    common_page = CommonPage(page)
    common_page.add_items_from_results_page(items_quantities_add, cart)
    # navigating to cart page
    page.reload()
    home_page.click_cart()
    cart_drawer = CartDrawer(page)
    cart_drawer.click_cart_page_button()
    cart_page = CartPage(page)
    # removing items from cart page
    cart_page.remove_multiple_items(cart, remove_indexes)

def test_remove_from_cart_drawer_minus_e2e(page, data):

    cart: list[dict[str, str | int | float]] = []
    items_quantities_add = data["items_quantities_add"]
    items_quantities_change = data["items_quantities_change"]
    url = data["url"]
    query = data["query"]

    page.goto(url)

    # home page
    home_page = HomePage(page)
    home_page.close_dialog()
    home_page.search_for(query)
    # clicking items in results page and adding them from item page
    common_page = CommonPage(page)
    common_page.add_items_from_results_page(items_quantities_add, cart)
    # navigating to cart drawer
    page.reload()
    home_page.click_cart()
    # decrease items in cart drawer
    cart_drawer = CartDrawer(page)
    cart_drawer.change_cart_quantities_cart_drawer(cart, items_quantities_change)
    cart_drawer.check_for_discount_and_update_cart(cart)
    cart_drawer.validate_items_in_cart(cart)

def test_remove_from_cart_drawer_delete_e2e(page, data):
    cart: list[dict[str, str | int | float]] = []
    items_quantities_add = data["items_quantities_add"]
    remove_indexes = data["remove_indexes"]
    url = data["url"]
    query = data["query"]

    page.goto(url)

    # home page
    home_page = HomePage(page)
    home_page.close_dialog()
    home_page.search_for(query)
    # clicking items in results page and adding them from item page
    common_page = CommonPage(page)
    common_page.add_items_from_results_page(items_quantities_add, cart)
    # navigating to cart drawer
    page.reload()
    home_page.click_cart()
    # removing items from cart drawer
    cart_page = CartPage(page)
    cart_page.remove_multiple_items(cart, remove_indexes)