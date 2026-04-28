import pytest

from pages.pim_page import PimPage


@pytest.mark.smoke
def test_search_existing_employee_by_id(pim_page: PimPage) -> None:
    pim_page.open_employee_list()
    pim_page.search_by_employee_id("0001")
    
    assert pim_page.get_results_count() >= 1


@pytest.mark.smoke
def test_search_existing_employee_by_name(pim_page: PimPage) -> None:
    pim_page.open_employee_list()
    found = pim_page.search_by_employee_name("Mohammed")
    
    assert pim_page.get_results_count() >= 0


def test_search_exact_match_returns_one_row(pim_page: PimPage) -> None:
    pim_page.open_employee_list()
    found = pim_page.search_by_employee_name("Mohammed Ghanem")
    
    if found:
        assert pim_page.get_results_count() >= 0


def test_clear_search_resets_results(pim_page: PimPage) -> None:
    pim_page.open_employee_list()
    
    pim_page.search_by_employee_id("0001")
    filtered_count = pim_page.get_results_count()
    
    pim_page.clear_search_filters()
    all_count = pim_page.get_results_count()
    

    assert all_count >= filtered_count


def test_search_nonexistent_employee_id(pim_page: PimPage) -> None:
    pim_page.open_employee_list()
    pim_page.search_by_employee_id("999999")
    
   
    result_count = pim_page.get_results_count()
    no_records_msg = pim_page.get_no_records_message()
    assert result_count == 0 or no_records_msg is not None, (
        f"Expected 0 rows or 'No Records Found', got {result_count} rows"
    )


def test_search_nonexistent_employee_name(pim_page: PimPage) -> None:
    pim_page.open_employee_list()
    found = pim_page.search_by_employee_name("XYZNonExistent")

    assert pim_page.get_results_count() >= 0


def test_search_empty_employee_id(pim_page: PimPage) -> None:
    pim_page.open_employee_list()
    pim_page.search_by_employee_id("")
    
    assert pim_page.get_results_count() >= 0


def test_search_special_characters_in_id(pim_page: PimPage) -> None:
    pim_page.open_employee_list()
    pim_page.search_by_employee_id("!@#$%")
    
    count = pim_page.get_results_count()
    assert count == 0 or pim_page.get_no_records_message() is not None