import re
from playwright.sync_api import Page, expect

## add employee test case 
def test_add_employee(page: Page) -> None:
    first_name ="Mohammed"
    last_name = "Ghanem"
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_role("textbox", name="Username").fill("Admin")
    page.get_by_role("textbox", name="Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("h6")).to_contain_text("Dashboard")
    page.get_by_role("link", name="PIM").click()
    expect(page.locator("h6")).to_contain_text("PIM")
    page.get_by_role("link", name="Add Employee").click()
    expect(page.get_by_role("heading", name="Add Employee")).to_be_visible()
    page.get_by_role("textbox", name="First Name").click()
    page.get_by_role("textbox", name="First Name").fill(first_name)
    page.get_by_role("textbox", name="Last Name").click()
    page.get_by_role("textbox", name="Last Name").fill(last_name)
    page.get_by_role("button", name="Save").click()
    expect(page.locator('h6:has-text("Personal Details")')).to_be_visible(timeout=10000)


