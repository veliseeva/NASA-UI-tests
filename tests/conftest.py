import os
import pytest
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selene import browser
from NASA_ui_project.utils import attach

load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def setup_browser():
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "123.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    server_ip = os.getenv('SELENOID_IP')
    assert server_ip is not None

    driver = webdriver.Remote(
        command_executor=f'http://{server_ip}:4444/wd/hub',
        options=options
    )

    browser.config.driver = driver
    browser.config.base_url = "https://images.nasa.gov"
    browser.config.timeout = 15
    browser.config.window_height = 1080
    browser.config.window_width = 1920

    yield

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()


@pytest.fixture(scope='function')
def mobile_browser(setup_browser):
    browser.driver.set_window_size(430, 932)

    yield
