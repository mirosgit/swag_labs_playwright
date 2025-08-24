from __future__ import annotations
from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url, wait_until="networkidle")

    def expect_url_contains(self, part: str):
        expect(self.page).to_have_url(lambda url: part in url)
