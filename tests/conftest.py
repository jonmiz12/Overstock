import os
from os.path import split

import allure
import pytest

from overstock.base_page import BasePage
from utils.utils import Utils


@pytest.fixture(autouse=True)
def before_and_after_each(request, page):
    page.set_default_timeout(7000)
    BasePage.failed_assertions.clear()
    Utils.create_test_folder_and_start_time(request)
    yield
    BasePage.create_logfile(request)
    BasePage.attach_test_artifacts()
    BasePage.print_failed_assertions()


def pytest_generate_tests(metafunc):
    # Check if the test function requires the "data" argument
    if "data" in metafunc.fixturenames:
        file_path = metafunc.definition.fspath.strpath
        test_name = metafunc.definition.originalname
        test_path = os.path.join(os.path.dirname(file_path), test_name)
        data = Utils.extract_test_data(str(test_path) + '.py')
        metafunc.parametrize("data", data)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if call.when == 'call':
        if report.failed:
            page = item.funcargs.get('page', None)
            file_name = "test_defect_screenshot.png"
            # BasePage.get_screenshot_in_test_report(page=page, file_name=file_name)
        else:
            # Force test failure based on failed assertions
            if hasattr(BasePage, 'failed_assertions') and BasePage.failed_assertions:
                pass
                # pytest.fail("This is a custom fail")

    if call.when == "teardown":
        if report.failed:
            assert False
        # If there are failed assertions and the test is not already marked as failed
        if hasattr(BasePage, 'failed_assertions') and BasePage.failed_assertions:
            if not report.failed:
                pass


