import pytest
from pageObjects.home_page import HomePage
from pageObjects.community_page import CommunityPage
from pageObjects.plan_page import PlanPage
from pageObjects.qmi_page import QMIPage
from pageObjects.search_results_page import SearchResultsPage


@pytest.mark.usefixtures("driver")
class TestSorting:
    def test_community_redirection(self, driver):
        home_page = HomePage(driver)
        community_page = CommunityPage(driver)

        chosenProductName = home_page.search("River", "community")
        community_page.verifyCorrectRedirection(chosenProductName)


    def test_qmi_redirection(self, driver):
        home_page = HomePage(driver)
        qmi_page = QMIPage(driver)

        chosenProductName = home_page.search("River", "qmi")
        qmi_page.verifyCorrectRedirection(chosenProductName)


    def test_plan_redirection(self, driver):
        home_page = HomePage(driver)
        plan_page = PlanPage(driver)

        chosenProductName = home_page.search("plan", "plan")
        plan_page.verifyCorrectRedirection(chosenProductName)


    def test_metro_redirection(self, driver):
        home_page = HomePage(driver)
        search_results_page = SearchResultsPage(driver)

        chosenProductName = home_page.search("River", "market")
        search_results_page.verifyCorrectRedirection(chosenProductName)