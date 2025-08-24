from __future__ import annotations

import re

from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage
from .components import Header

class InventoryPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url
        self.header = Header(page)
        self.sort_select: Locator = page.locator(".product_sort_container")
        self.items: Locator = page.locator(".inventory_list .inventory_item")
        self.item_names: Locator = page.locator(".inventory_item_name")
        self.item_prices: Locator = page.locator(".inventory_item_price")

    def open(self):
        self.goto(f"{self.base_url}/inventory.html")
        expect(self.items.first).to_be_visible()

    def add_item_by_name(self, name: str):
        card = self.page.locator(".inventory_item").filter(
            has=self.page.locator(".inventory_item_name", has_text=name)
        )

        btn = card.locator(".btn_primary.btn_inventory")
        if btn.count() == 0:
            btn = card.get_by_role("button", name=re.compile(r"^\s*add to cart\s*$", re.I))

        expect(btn.first).to_be_visible()
        btn.first.click()


    def sort_by(self, visible_text: str):
        self.sort_select.select_option(label=visible_text)

    def get_names(self) -> list[str]:
        return [e.strip() for e in self.item_names.all_text_contents()]

    def get_prices(self) -> list[float]:
        raw = self.item_prices.all_text_contents()
        return [float(x.replace("$", "").strip()) for x in raw]
