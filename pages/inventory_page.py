from playwright.sync_api import Page


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_role("heading", name="Inventory")
        self.search = page.get_by_label("Search inventory")

    def item_names(self) -> list[str]:
        return self.page.locator("[data-testid='item-name']").all_text_contents()

    def search_for(self, term: str) -> None:
        self.search.fill(term)
