import pytest
from playwright.sync_api import Page

from overstock.basePage import BasePage
from utils.utils import Utils


@pytest.fixture(autouse=True)
def before_and_after_each(request):
    BasePage.failed_assertions.clear()
    Utils.create_test_folder_and_start_time(request)
    yield
    BasePage.create_logfile(request)
    BasePage.print_failed_assertions()

