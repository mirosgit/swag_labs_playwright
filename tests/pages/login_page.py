from __future__ import annotations
from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url
        self.username: Locator = page.locator("#user-name")
        self.password: Locator = page.locator("#password")
        self.login_btn: Locator = page.locator("#login-button")
        self.error_box: Locator = page.locator("[data-test='error'], .error-message-container")

    def open(self):
        self.goto(f"{self.base_url}/index.html")

    def login(self, user: str, pwd: str):
        self.username.fill(user)
        self.password.fill(pwd)
        self.login_btn.click()

    def expect_error(self):
        expect(self.error_box).to_be_visible()
