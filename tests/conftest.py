import pytest

from overstock.basePage import BasePage
from utils.utils import Utils


@pytest.fixture(autouse=True)
def before_and_after_each(request, page):
    BasePage.failed_assertions.clear()
    Utils.create_test_folder_and_start_time(request)
    yield
    BasePage.create_logfile(request)
    BasePage.print_failed_assertions()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get('page', None)
        if page:
            file_name = "test_defect_screenshot.png"
            BasePage.get_screenshot_in_test_report(page=page, file_name=file_name)
