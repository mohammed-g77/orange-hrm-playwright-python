import re

from playwright.sync_api import Page, expect


class PersonalDetailsPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def should_be_loaded(self) -> None:
        expect(self.page).to_have_url(
            re.compile(r".*/pim/viewPersonalDetails/empNumber/\d+$"),
            timeout=15000,
        )
        expect(
            self.page.get_by_role("heading", name="Personal Details")
        ).to_be_visible(timeout=15000)
