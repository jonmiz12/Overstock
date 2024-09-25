from playwright.sync_api import Page

from overstock.basePage import BasePage


def test_responses(page: Page):
    # pre-decided 'valid' response statuses
    # 200 successful request
    # 201 successful request, resource created
    # 204 successful request, no content is returned
    valid_responses = [200, 201, 204]

    # Starts listening for responses
    responses = []

    page.on("response", lambda response: responses.append(response))

    page.goto("https://www.overstock.com/")

    # Extract the failed responses
    base_page = BasePage(page)
    base_page.assert_responses(responses, valid_responses)
