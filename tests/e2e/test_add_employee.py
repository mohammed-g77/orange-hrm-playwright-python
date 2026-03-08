from pages.personal_details_page import PersonalDetailsPage
from pages.pim_page import PimPage


def test_add_employee_without_login_details(
    pim_page: PimPage,
    employee_data: dict[str, str],
) -> None:
    pim_page.open_add_employee()
    pim_page.add_employee_without_login_details(
        first_name=employee_data["first_name"],
        last_name=employee_data["last_name"],
    )

    personal_details_page = PersonalDetailsPage(pim_page.page)
    personal_details_page.should_be_loaded()


def test_add_employee_with_login_details(
    pim_page: PimPage,
    employee_data: dict[str, str],
) -> None:
    pim_page.open_add_employee()
    pim_page.add_employee_with_login_details(
        first_name=employee_data["first_name"],
        last_name=employee_data["last_name"],
        username=employee_data["username"],
        password=employee_data["password"],
    )

    personal_details_page = PersonalDetailsPage(pim_page.page)
    personal_details_page.should_be_loaded()
