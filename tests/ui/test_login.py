import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config import base_url


@pytest.mark.smoke
def test_valid_user_can_sign_in(page):
    login = LoginPage(page, base_url())
    inventory = InventoryPage(page)

    login.open()
    login.login_as("demo_user", "quality123")

    inventory.heading.wait_for()
    assert page.url.endswith("/inventory")


@pytest.mark.regression
def test_invalid_credentials_show_clear_error(page):
    login = LoginPage(page, base_url())

    login.open()
    login.login_as("wrong_user", "wrong_password")

    assert login.error_message.text_content() == "Invalid username or password"
    assert page.url.rstrip("/") == base_url()
