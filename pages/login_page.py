from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

        self.username = page.get_by_label("Username")
        self.password = page.get_by_label("Password")
        self.sign_in_button = page.get_by_role("button", name="Sign in")
        self.error_message = page.get_by_role("alert")

    def open(self) -> None:
        self.page.goto(f"{self.base_url}/")

    def login_as(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.sign_in_button.click()
