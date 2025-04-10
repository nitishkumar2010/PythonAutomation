import pytest
from pageObjects.home_page import HomePage
from pageObjects.community_page import CommunityPage
from pageObjects.plan_page import PlanPage
from pageObjects.qmi_page import QMIPage
from pageObjects.search_results_page import SearchResultsPage


@pytest.mark.usefixtures("driver")
class TestSorting:

    def test_community_default_sort(self, driver):

        home_page = HomePage(driver)
        search_results_page = SearchResultsPage(driver)

        home_page.search("phoenix", "market")
        search_results_page.apply_sort_option("$ - $$$")
        search_results_page.verify_sort_functionality_for_community_cards(True)

    def test_community_default_sort_2(self, driver):

        home_page = HomePage(driver)
        search_results_page = SearchResultsPage(driver)

        home_page.click_on_location_from_FYH_header("Florida")

        search_results_page.apply_sort_option("$ - $$$")
        search_results_page.verify_sort_functionality_for_community_cards(True)
        search_results_page.verify_master_planned_comm_sort(True)
