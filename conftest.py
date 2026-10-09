import os
import time
import random
import logging
import pytest
from dotenv import load_dotenv
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from selene import browser
from utils import attach


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(autouse=True)
def slow_down_tests():
    yield
    time.sleep(random.uniform(4.0, 8.0))


@pytest.fixture(scope='function', autouse=True)
def setup_browser(load_env):
    options = Options()
    # Оптимизация скорости (не ждем загрузку тяжелой статики и аналитики NASA)
    options.page_load_strategy = 'eager'
    # === Настройки стабильности для Docker/CI (Selenoid) ===
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage") # Решает проблему нехватки памяти в контейнере
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=VizDisplayCompositor") # Предотвращает падение рендерера Chrome
    # === Изоляция и чистый стейт ===
    options.add_argument("--incognito")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-session-crashed-bubble")
    # === Обход Anti-Bot защиты (NASA WAF) ===
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "123.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True,
            "sessionTimeout": "5m"
        }
    }
    options.capabilities.update(selenoid_capabilities)

    server_ip = os.getenv('SELENOID_IP')
    assert server_ip is not None

    driver = webdriver.Remote(
        command_executor=f'http://{server_ip}:4444/wd/hub',
        options=options
    )
    driver.set_page_load_timeout(60)

    browser.config.driver = driver
    browser.config.base_url = "https://images.nasa.gov"
    browser.config.timeout = 60
    browser.config.window_height = 1080
    browser.config.window_width = 1920

    yield

    session_id = browser.driver.session_id

    try:
        attach.add_screenshot(browser)
        attach.add_logs(browser)
        attach.add_html(browser)
    except WebDriverException as e:
        logging.error(f"Ошибка при сборе артефактов браузера: {e}")

    try:
        browser.quit()
    except WebDriverException as e:
        logging.error(f"Ошибка при закрытии браузера: {e}")

    attach.add_video(session_id)
