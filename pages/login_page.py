from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url

    def open(self) -> None:
        self.page.goto(f"{self.base_url}/auth/login")
        expect(self.page).to_have_url(f"{self.base_url}/auth/login")

    def login(self, username: str, password: str) -> None:
        self.page.get_by_role("textbox", name="Username").fill(username)
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="Login").click()
        expect(self.page.get_by_role("heading", name="Dashboard")).to_be_visible()
