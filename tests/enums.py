from __future__ import annotations
import os
from enum import StrEnum

class Routes(StrEnum):
    INDEX = "/index.html"
    INVENTORY = "/inventory.html"
    CART = "/cart.html"
    CHECKOUT_INFO = "/checkout-step-one.html"
    CHECKOUT_OVERVIEW = "/checkout-step-two.html"
    CHECKOUT_COMPLETE = "/checkout-complete.html"

class SortOption(StrEnum):
    NAME_AZ = "Name (A to Z)"
    NAME_ZA = "Name (Z to A)"
    PRICE_LOW_HIGH = "Price (low to high)"
    PRICE_HIGH_LOW = "Price (high to low)"

class ItemName(StrEnum):
    BACKPACK = "Sauce Labs Backpack"
    BIKE_LIGHT = "Sauce Labs Bike Light"
    BOLT_TSHIRT = "Sauce Labs Bolt T-Shirt"
    FLEECE_JACKET = "Sauce Labs Fleece Jacket"

class Users:
    STD_USER = os.getenv("STD_USER", "standard_user")
    STD_PASS = os.getenv("STD_PASS", "secret_sauce")
    LOCKED_USER = os.getenv("LOCKED_USER", "locked_out_user")
    LOCKED_PASS = os.getenv("LOCKED_PASS", "secret_sauce")
