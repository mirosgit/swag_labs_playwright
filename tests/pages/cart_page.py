from __future__ import annotations
from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url
        self.cart_items: Locator = page.locator(".cart_list .cart_item")
        self.checkout_btn: Locator = page.locator("a.btn_action.checkout_button")

    def open(self):
        self.goto(f"{self.base_url}/cart.html")
        expect(self.cart_items.first).to_be_visible()

    def item_names(self) -> list[str]:
        return [t.strip() for t in self.page.locator(".inventory_item_name").all_text_contents()]

    def checkout(self):
        self.checkout_btn.click()
