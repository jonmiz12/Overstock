# Overstock Automation Project

This project automates tests for [overstock.com](https://www.overstock.com). It covers various flows for adding and removing products, validating key sections, and checking response integrity on the site.
## Recommended prerequisites
  - **Python version - 3.10.11**
  - **Playwright version - 9.6.6**

## Known issues

### Unknown maximum quantities
- **Different items have different maximum quantities allowed. The maximum quantities are un-known, only after trying to exceed this unknown amount, an error is displayed.**

### Cart prices decimal anomalies
- **Scaling the cart's total amount over around 10,000$ can lead to price validation errors due to the site calculating floating numbers with longer decimal length than is actually displayed.**
- **Therefore, the project validates prices calculations without floating points by default.**

## Reports
- **The project generates a folder for each test in the `/reports` folder. It creates a log that contains the failed assertions collected throughout the test and screenshots taken while the failed assertions occurred.**

- **The logs and screenshots can be viewed conveniently using allure by executing the following command at the directory the test was executed in.**
- `allure serve reports/allure`

## Project Structure
### locators
- **cart_drawer.json**: Locators for interacting with the cart drawer.
- **cart_page.json**: Locators for interacting with the cart page.
- **header.json**: Locators for interacting with the site’s header.
- **home_page.json**: Locators for interacting with the home page.
- **item_page.json**: Locators interacting with the item page.
- **results_page.json**: Locators for interacting with the results page.
### Pages
- **cart_drawer.py**: Methods interacting with the cart drawer.
- **cart_page.py**: Methods interacting with the cart page.
- **header.py**: Methods interacting with the site’s header.
- **home_page.py**: Methods interacting with the home page.
- **item_page.py**: Methods interacting with the item page.
- **results_page.py**: Methods interacting with the results page.

### Core Modules
- **base_page.py**: Contains common methods shared across all page objects.
- **common_cart.py**: Groups common methods for both cartDrawer.py and cartPage.py.
- **common_page.py**: Groups common methods that utilize instances of multiple pages.

### Tests (Test cases)
#### test_add_products.py
- **test_add_from_cart_drawer_e2e**: Tests adding items via the cart drawer.
- **test_add_from_cart_page_e2e**: Tests adding items via the cart page.
- **test_add_from_item_page_e2e**: Tests adding items via the item detail page.

#### test_remove_products.py
- **test_remove_from_cart_drawer_delete_e2e**: Tests removing items using the bin button in the cart drawer.
- **test_remove_from_cart_drawer_minus_e2e**: Tests removing items via the minus button in the cart drawer.
- **test_removeFromCartPageDelete_e2e**: Tests removing items using the bin button on the cart page.
- **test_remove_from_cart_page_minus_e2e**: Tests removing items via the minus button on the cart page.

#### Other Tests
- **test_add_and_remove_products_e2e.py**: Comprehensive test combining add and remove operations.
- **test_home_page_sections.py**: Validates presence of home page sections.
- **test_responses.py**: Checks for bad responses on the home page.
- **test_search_bar.py**: Tests search functionality and result validation.

### Utilities
- **utils.py**: Provides utility methods for file handling and data extraction.
## test_data
- **contains a json file for each test.**
- **Each file must contain at least one object with the relevant keys and values for the test to execute.**
- **The test will execute the number times as the number of objects in its json file.**

### requirements
- **`requirements.txt` is a file that contains the versions of the tools and packages required in this project**

### pytest.ini
- **`pytest.ini` contains the pytest configuration such as reports conffigurations, browser, resolution, etc.**

## Running the tests
### Use the "pytest" command to run tests. e.g -
- **`pytest tests` to run all tests**
- **`pytest tests\add_products` to run "add_products" tests folder**
- **`pytest tests\add_products\test_addFromCartDrawer.py` to run "test_addFromCartDrawer.py"**

