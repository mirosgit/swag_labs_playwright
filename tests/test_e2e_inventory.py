import allure

from tests.pages import (
    LoginPage,
    InventoryPage,
    CartPage,
    CheckoutInfoPage,
    CheckoutOverviewPage,
    CheckoutCompletePage,
)
from tests.enums import SortOption, ItemName, Users

def do_login(page, base_url, user, pwd):
    lp = LoginPage(page, base_url)
    with allure.step("Open login page"):
        lp.open()
    with allure.step(f"Login as {user}"):
        lp.login(user, pwd)

@allure.title("Login success and logout")
@allure.story("Auth")
def test_login_success_and_logout(page, base_url):
    do_login(page, base_url, Users.STD_USER, Users.STD_PASS)
    inv = InventoryPage(page, base_url)
    inv.open()
    with allure.step("Logout from burger menu"):
        inv.header.logout()

@allure.title("Inventory sorting by price asc/desc")
@allure.story("Catalog")
def test_inventory_sorting(page, base_url):
    do_login(page, base_url, Users.STD_USER, Users.STD_PASS)
    inv = InventoryPage(page, base_url)
    inv.open()

    with allure.step("Sort by Price (low to high) and assert ascending"):
        inv.sort_by(SortOption.PRICE_LOW_HIGH)
        prices = inv.get_prices()
        assert prices == sorted(prices)

    with allure.step("Sort by Price (high to low) and assert descending"):
        inv.sort_by(SortOption.PRICE_HIGH_LOW)
        prices_desc = inv.get_prices()
        assert prices_desc == sorted(prices_desc, reverse=True)

@allure.title("Add to cart and verify badge + items")
@allure.story("Cart")
def test_add_to_cart_and_badge(page, base_url):
    do_login(page, base_url, Users.STD_USER, Users.STD_PASS)
    inv = InventoryPage(page, base_url)
    inv.open()

    with allure.step("Add two items to cart"):
        inv.add_item_by_name(ItemName.BACKPACK)
        inv.add_item_by_name(ItemName.BIKE_LIGHT)
        assert inv.header.get_cart_count() == 2

    with allure.step("Open cart and assert items present"):
        inv.header.open_cart()
        cart = CartPage(page, base_url)
        names = cart.item_names()
        assert ItemName.BACKPACK in names and ItemName.BIKE_LIGHT in names

@allure.title("Full checkout flow")
@allure.story("Checkout")
def test_full_checkout_flow(page, base_url):
    do_login(page, base_url, Users.STD_USER, Users.STD_PASS)
    inv = InventoryPage(page, base_url)
    inv.open()
    with allure.step("Add two items"):
        inv.add_item_by_name(ItemName.BACKPACK)
        inv.add_item_by_name(ItemName.BOLT_TSHIRT)

    with allure.step("Go to cart and start checkout"):
        inv.header.open_cart()
        cart = CartPage(page, base_url)
        cart.checkout()

    with allure.step("Fill user info"):
        info = CheckoutInfoPage(page, base_url)
        info.fill_and_continue(first="QA", last="Engineer", zip_code="01001")

    with allure.step("Finish overview"):
        ov = CheckoutOverviewPage(page, base_url)
        ov.finish()

    with allure.step("Expect success page"):
        cc = CheckoutCompletePage(page, base_url)
        cc.expect_success()

@allure.title("Login failure of locked user shows error")
@allure.story("Auth")
def test_login_failure_locked_user(page, base_url):
    lp = LoginPage(page, base_url)
    lp.open()
    lp.login(Users.LOCKED_USER, Users.LOCKED_PASS)
    lp.expect_error()
