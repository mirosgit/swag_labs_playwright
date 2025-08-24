from __future__ import annotations
from playwright.sync_api import Page, Locator, expect

class Header:
    def __init__(self, page: Page):
        self.page = page
        self.cart_link: Locator = page.locator(".shopping_cart_link")
        self.cart_badge: Locator = page.locator(".shopping_cart_badge")
        self.menu_btn: Locator = page.locator("#menu_button_container button", has_text="Open Menu")
        self.logout_link: Locator = page.locator("#logout_sidebar_link")

    def open_cart(self):
        self.cart_link.click()

    def get_cart_count(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.first.text_content())

    def logout(self):
        self.menu_btn.click()
        self.logout_link.click()
        expect(self.page.locator("#login-button")).to_be_visible()
