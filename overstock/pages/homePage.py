from overstock.pages.header import Header
from playwright.sync_api import Page


class HomePage(Header):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.close_dialog_btn = page.locator("#cl-dialog-close")
        self.sections = page.locator("#main-content [id^='shopify-section']")

    def close_dialog(self):
        if self.close_dialog_btn.is_visible():
            self.close_dialog_btn.click(timeout=500)

    def validate_home_page_sections(self, expected_sections_count: int = 6):
        actual_sections_count = self.sections.count()
        if actual_sections_count != expected_sections_count:
            error = f"Expected sections count: {expected_sections_count}. actual sections count: {actual_sections_count}"
            self.add_failed_assertion(error)
            self.get_screenshot_in_test_report()
