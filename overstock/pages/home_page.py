import inspect
import json
import os

from overstock.pages.header import Header
from playwright.sync_api import Page

from utils.utils import Utils

class HomePage(Header):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        locators_path = Utils.convert_to_locators_directory(__file__)
        with open(locators_path, "r") as file:
            locators = json.load(file)
        for key, value in locators.items():
            setattr(self, key, page.locator(value))

    def validate_home_page_sections(self, expected_sections_count: int):
        actual_sections_count = self.sections.count()
        if actual_sections_count != expected_sections_count:
            error = f"Expected sections count: {expected_sections_count}. actual sections count: {actual_sections_count}"
            self.add_failed_assertion(error, inspect.currentframe().f_code.co_name)
            self.get_screenshot_in_test_report()