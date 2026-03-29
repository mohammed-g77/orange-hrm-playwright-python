from playwright.sync_api import Page, expect


class PimPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> None:
        self.page.get_by_role("link", name="PIM").click()
        expect(self.page.get_by_role("heading", name="PIM")).to_be_visible()

    def open_add_employee(self) -> None:
        self.page.get_by_role("link", name="Add Employee").click()
        expect(self.page.get_by_role("heading", name="Add Employee")).to_be_visible()

    def add_employee_without_login_details(
        self,
        first_name: str,
        last_name: str,
    ) -> None:
        self._fill_employee_name(first_name=first_name, last_name=last_name)
        self.page.get_by_role("button", name="Save").click()

    def add_employee_with_login_details(
        self,
        first_name: str,
        last_name: str,
        username: str,
        password: str,
    ) -> None:
        self._fill_employee_name(first_name=first_name, last_name=last_name)
        self._enable_login_details()

        username_input = self.page.locator(
            "//label[normalize-space()='Username']"
            "/ancestor::div[contains(@class,'oxd-input-group')]//input"
        )
        password_input = self.page.locator(
            "(//label[normalize-space()='Password']"
            "/ancestor::div[contains(@class,'oxd-input-group')]//input)[1]"
        )
        confirm_password_input = self.page.locator(
            "//label[normalize-space()='Confirm Password']"
            "/ancestor::div[contains(@class,'oxd-input-group')]//input"
        )

        expect(username_input).to_be_visible()
        expect(password_input).to_be_visible()
        expect(confirm_password_input).to_be_visible()

        username_input.fill(username)
        password_input.fill(password)
        confirm_password_input.fill(password)

        print("Username entered:", username_input.input_value())
        print("Password entered:", password_input.input_value())
        print("Confirm password entered:", confirm_password_input.input_value())

        self.page.wait_for_timeout(1500)
        self.page.get_by_role("button", name="Save").click()
        self.page.wait_for_timeout(1500)

        print("Current URL:", self.page.url)

        errors = self.page.locator("span.oxd-input-field-error-message")
        print("Validation errors count:", errors.count())
        for i in range(errors.count()):
            print("Validation error:", errors.nth(i).inner_text())

    def _fill_employee_name(self, first_name: str, last_name: str) -> None:
        self.page.get_by_role("textbox", name="First Name").fill(first_name)
        self.page.get_by_role("textbox", name="Last Name").fill(last_name)

    def _enable_login_details(self) -> None:
        self.page.locator("span.oxd-switch-input").click()
        expect(
            self.page.locator(
                "//label[normalize-space()='Username']"
                "/ancestor::div[contains(@class,'oxd-input-group')]//input"
            )
        ).to_be_visible()
