from datetime import datetime

import pytest
import os
from pathlib import Path
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pytest_html import extras
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def slugify(value):
    """Converts test nodeid into a filename-friendly format."""
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', value)


@pytest.fixture(scope="function")
def driver():
    """Setup WebDriver before each test and quit after."""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get("https://mattamyhomes.com/?country=USA")

    yield driver  # Return driver instance to test

    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot on test failure and attach it to the pytest-html report."""
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":

        if "driver" in item.funcargs:
            driver = item.funcargs["driver"]
            current_url = driver.current_url  # ✅ Get the current page URL

            # Attach URL to HTML report
            extra.append(pytest_html.extras.url(current_url, "Page URL"))


        if report.failed and "driver" in item.funcargs:
            driver = item.funcargs["driver"]

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            # ✅ FIX: Ensure screenshots go inside "reports/screenshots/"
            base_dir = Path("reports")  # Always start inside "reports"
            screenshot_dir = base_dir / "screenshots"
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            # ✅ FIX: Correct relative path for image attachment
            file_name = f"{slugify(item.nodeid)}_{timestamp}.png"
            full_path = screenshot_dir / file_name
            relative_path = f"screenshots/{file_name}"  # Ensure correct HTML path

            driver.save_screenshot(str(full_path))
            print(f"📸 Screenshot saved at: {full_path}")

            # ✅ Attach screenshot to HTML report with correct relative path
            extra.append(pytest_html.extras.image(str(full_path), "Screenshot"))
            extra.append(pytest_html.extras.html(f'<a href="{str(full_path)}" target="_blank">🔍 View Screenshot</a>'))

        report.extra = extra


def pytest_html_report_title(report):
    """Set a custom title for the pytest-html report."""
    report.title = "Automation Framework Test Report"


@pytest.hookimpl(tryfirst=True)
def pytest_html_results_summary(prefix, summary, postfix):
    """Customize the summary section of the report."""
    prefix.extend([
        "<p><strong>Project:</strong> Mattamy Homes</p>",
        "<p><strong>Tester:</strong> Nitish</p>"
    ])

def pytest_addoption(parser):
    """Add command-line option to specify the report directory."""
    parser.addoption(
        "--report-dir",
        action="store",
        default="reports",
        help="Specify the directory to save HTML reports.",
    )

def pytest_configure(config):
    """Configure report filename."""
    # timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    timestamp = datetime.now().strftime("%Y-%m-%d")
    report_filename = f"report_{timestamp}.html"
    config.option.htmlpath = os.path.join(os.getcwd(), report_filename) #This line is changed.