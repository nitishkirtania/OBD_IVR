import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from Global_Key import USERNAME, PASSWORD, Base_url  # Import credentials

class WebDriverExample:
    def __init__(self, driver):
        self.driver = driver

    def wait_and_click(self, by_locator):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(by_locator)).click()

@pytest.mark.usefixtures("driver")  # Ensure driver fixture is used
def test_login(driver):
    """Perform login."""
    driver.get(Base_url)
    wait = WebDriverWait(driver, 20)

    username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='mat-input-0']")))
    password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='mat-input-1']")))
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    time.sleep(2)  # Avoid excessive sleeps, but some pages need minor delays
    login_button.click()

    wait.until(EC.title_is("IVR"))
    assert driver.title == "IVR", f"Expected title 'IVR', but got '{driver.title}'"
    print("Login test completed successfully.")
