# Overstock Automation Project

This project automates tests for [overstock.com](https://www.overstock.com). It covers various flows for adding and removing products, validating key sections, and checking response integrity on the site.
## Recommended prerequisites
  - **Python version - 3.10.11**
  - **Playwright version - 9.6.6**

## Known issues

### Unknown maximum quantities
- **Different items have different maximum quantities allowed. The maximum quantities are un-known, only after trying to exceed this unknown amount is when an error is displayed**

### Cart prices decimal anomalies
- **Scaling the cart's total amount over around 10,000$ can lead to price validation errors due to the site calculating floating numbers with longer decimal length than is actually displayed**
- **Therefore, the project validates prices calculations without floating points by default**

## Reports
The project generates detailed logs and screenshots for each test in the `/reports` folder. Each test run automatically creates a log file to record any errors and includes screenshots of failed steps.

## Project Structure

### Pages
- **cartDrawer.py**: Methods interacting with the cart drawer.
- **cartPage.py**: Methods interacting with the cart page.
- **header.py**: Methods interacting with the site’s header.
- **homePage.py**: Methods interacting with the home page.
- **itemPage.py**: Methods interacting with the item page.
- **resultsPage.py**: Methods interacting with the results page.

### Core Modules
- **basePage.py**: Contains common methods shared across all page objects.
- **commonCart.py**: Groups common methods for both cartDrawer.py and cartPage.py.

### Tests (Test cases)
#### Add Products
- **test_addFromCartDrawer.py**: Tests adding items via the cart drawer.
- **test_addFromCartPage.py**: Tests adding items via the cart page.
- **test_addFromItemPage.py**: Tests adding items via the item detail page.

#### Remove Products
- **test_removeFromCartDrawerDelete.py**: Tests removing items using the bin button in the cart drawer.
- **test_removeFromCartDrawerMinus.py**: Tests removing items via the minus button in the cart drawer.
- **test_removeFromCartPageDelete.py**: Tests removing items using the bin button on the cart page.
- **test_removeFromCartPageMinus.py**: Tests removing items via the minus button on the cart page.

#### Other Tests
- **test_addAndRemoveProducts.py**: Comprehensive test combining add and remove operations.
- **test_homePageSections.py**: Validates presence of home page sections.
- **test_responses.py**: Checks for bad responses on the home page.
- **test_searchBar.py**: Tests search functionality and result validation.

### Utilities
- **search_queries.json**: Contains search query data for the search bar tests.
- **utils.py**: Provides utility methods for file handling and data extraction.

## Running the tests
### Use the "pytest" command to run tests. e.g -
- **`pytest tests` to run all tests**
- **`pytest tests\add_products` to run "add_products" tests folder**
- **`pytest tests\add_products\test_addFromCartDrawer.py` to run "test_addFromCartDrawer.py"**

