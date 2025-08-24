from __future__ import annotations

import re

from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage
from faker import Faker

fake = Faker()

class CheckoutInfoPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url
        self.first: Locator = page.locator("#first-name")
        self.last:  Locator = page.locator("#last-name")
        self.zip:   Locator = page.locator("#postal-code")
        self.continue_btn: Locator = page.locator("div.checkout_buttons > input")

    def fill_and_continue(self, first: str | None = None, last: str | None = None, zip_code: str | None = None):
        first = first or fake.first_name()
        last = last or fake.last_name()
        zip_code = zip_code or fake.postcode()

        self.first.fill(first)
        self.last.fill(last)
        self.zip.fill(zip_code)

        expect(self.continue_btn).to_be_visible()
        self.continue_btn.click()

class CheckoutOverviewPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url
        self.finish_btn: Locator = page.locator("a.btn_action.cart_button")

    def finish(self):
        self.finish_btn.click()

class CheckoutCompletePage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url
        self.complete_header: Locator = page.locator(".complete-header")

    def expect_success(self):
        expect(self.complete_header).to_have_text(re.compile("THANK YOU FOR YOUR ORDER", re.I))
