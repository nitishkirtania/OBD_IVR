import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException
import time

@pytest.fixture(scope="session")  # Set to "session" so it runs once per test session
def driver():
    retries = 3
    wait_time = 5
    attempt = 0
    driver = None

    while attempt < retries:
        try:
            print(f"Attempting to initialize WebDriver (Attempt {attempt + 1})...")
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            print("WebDriver initialized successfully.")
            driver.maximize_window()
            yield driver  # Provide driver to test
            print("Closing the WebDriver")
            driver.quit()
            break
        except WebDriverException as e:
            print(f"WebDriver initialization failed: {e}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                pytest.fail(f"Failed to initialize WebDriver after {retries} attempts.")
