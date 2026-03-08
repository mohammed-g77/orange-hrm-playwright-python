import uuid

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.pim_page import PimPage

BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php"
ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "admin123"


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page=page, base_url=BASE_URL)


@pytest.fixture
def pim_page(page: Page, login_page: LoginPage) -> PimPage:
    login_page.open()
    login_page.login(username=ADMIN_USERNAME, password=ADMIN_PASSWORD)
    pim = PimPage(page)
    pim.open()
    return pim


@pytest.fixture
def employee_data() -> dict[str, str]:
    suffix = uuid.uuid4().hex[:6]
    return {
        "first_name": f"Mohammed{suffix[:3]}",
        "last_name": f"Ghanem{suffix[3:]}",
        "username": f"mgh_{suffix}",
        "password": f"Qa@{suffix}123",
    }
