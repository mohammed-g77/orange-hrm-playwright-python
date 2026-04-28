from playwright.sync_api import Page, expect


class PimPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> None:
        self.page.get_by_role("link", name="PIM").click()
        self.page.wait_for_url("**/pim/viewEmployeeList", timeout=30000)
        expect(self.page.get_by_role("heading", name="PIM")).to_be_visible(timeout=15000)

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

        self.page.get_by_role("button", name="Save").click()
        self.page.wait_for_url("**/pim/viewPersonalDetails/empNumber/**", timeout=30000)

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

    # ------------------------------------------------------------------ #
    # Employee List / Search methods
    # ------------------------------------------------------------------ #

    def open_employee_list(self) -> None:
        """Navigate to the Employee List view and wait for the table."""
        self.page.wait_for_url("**/pim/viewEmployeeList", timeout=3000)
        expect(
            self.page.locator(".oxd-table-body")
        ).to_be_visible(timeout=3000)

    def search_by_employee_id(self, employee_id: str) -> None:
        """Fill the Employee Id field and submit the search form."""
        id_input = self.page.locator(
            "//label[normalize-space()='Employee Id']"
            "/ancestor::div[contains(@class,'oxd-input-group')]//input"
        )
        expect(id_input).to_be_visible(timeout=2000)
        id_input.clear()
        id_input.fill(employee_id)
        self.page.get_by_role("button", name="Search").click()
        self.page.wait_for_load_state("networkidle", timeout=5000)

    def search_by_employee_name(self, name: str) -> bool:
        """Fill the Employee Name autocomplete and submit the search form.

        Returns True if the autocomplete suggestion was selected, False if
        the name was simply typed (no suggestion appeared).
        """
        name_input = self.page.locator(
            "//label[normalize-space()='Employee Name']"
            "/ancestor::div[contains(@class,'oxd-input-group')]//input"
        )
        expect(name_input).to_be_visible(timeout=2000)
        name_input.clear()
        name_input.type(name, delay=80)

        # Wait briefly for the autocomplete dropdown
        dropdown_option = self.page.locator(".oxd-autocomplete-dropdown .oxd-autocomplete-option").first
        try:
            dropdown_option.wait_for(state="visible", timeout=5000)
            dropdown_option.click()
            selected = True
        except Exception:
            selected = False

        self.page.get_by_role("button", name="Search").click()
        self.page.wait_for_load_state("networkidle", timeout=5000)
        return selected

    def get_results_count(self) -> int:
        """Return the number of data rows currently shown in the results table.

        Returns 0 when the search yields no results (i.e. 'No Records Found').
        """
        self.page.wait_for_load_state("networkidle", timeout=5000)
        # Wait until the loading spinner is gone (table has settled)
        self.page.locator(".oxd-loading-spinner").wait_for(state="hidden", timeout=5000)
        return self.page.locator(".oxd-table-body .oxd-table-row").count()

    def get_no_records_message(self) -> str | None:
        """Return the 'No Records Found' message text, or None if absent."""
        locator = self.page.locator(".oxd-text", has_text="No Records Found")
        try:
            locator.wait_for(state="visible", timeout=5000)
            return locator.inner_text()
        except Exception:
            return None

    def clear_search_filters(self) -> None:
        """Click the Reset button to restore default search results."""
        self.page.get_by_role("button", name="Reset").click()
        self.page.wait_for_load_state("networkidle", timeout=5000)
