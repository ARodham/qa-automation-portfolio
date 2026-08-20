import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config import base_url


@pytest.fixture
def signed_in_inventory(page) -> InventoryPage:
    login = LoginPage(page, base_url())
    inventory = InventoryPage(page)

    login.open()
    login.login_as("demo_user", "quality123")
    inventory.heading.wait_for()

    return inventory


@pytest.mark.smoke
def test_inventory_displays_expected_items(signed_in_inventory: InventoryPage):
    assert signed_in_inventory.item_names() == [
        "Wireless Headset",
        "Mechanical Keyboard",
        "USB-C Dock",
    ]


@pytest.mark.regression
def test_inventory_search_filters_results(signed_in_inventory: InventoryPage):
    signed_in_inventory.search_for("keyboard")

    assert signed_in_inventory.item_names() == ["Mechanical Keyboard"]
