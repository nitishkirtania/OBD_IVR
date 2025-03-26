import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import shutil
from test_Login import WebDriverExample, test_login
from Global_Key import Prompt_file


class PromptHandler(WebDriverExample):
    """Handles Prompt operations like navigation and file upload."""

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def navigate_to_prompt_data(self):
        """Navigate to the Prompt Data page after login."""
        prompt_page = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Prompt"))
        )

        self.driver.execute_script("arguments[0].scrollIntoView();", prompt_page)
        time.sleep(5)

        try:
            prompt_page.click()
        except:
            self.driver.execute_script("arguments[0].click();", prompt_page)

    def add_audio_prompt(self):
        """Add new Audio Prompt."""
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "ngx-overlay"))
        )

        add_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add Prompt']"))
        )
        add_button.click()

        prompt_file_dy, extension = os.path.splitext(Prompt_file)
        timestamp = time.strftime("%Y%m%d%H%M%S")
        dynamic_filename = f"{prompt_file_dy}_{timestamp}{extension}"
        shutil.copy(Prompt_file, dynamic_filename)
        time.sleep(3)

        file_upload_field = self.driver.find_element(By.XPATH, "//div//input[@id='upload-0']")
        file_upload_field.send_keys(dynamic_filename)
        time.sleep(3)

        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit']"))
        )
        submit_button.click()
        time.sleep(3)


@pytest.mark.usefixtures("driver")
def test_prompt_data_operations(driver):
    """Test Prompt Data addition flow with window handling."""
    test_login(driver)

    if not driver.window_handles:
        pytest.fail("No active browser window found. Test aborted.")

    driver.switch_to.window(driver.window_handles[-1])

    prompt_handler = PromptHandler(driver)
    prompt_handler.navigate_to_prompt_data()
    prompt_handler.add_audio_prompt()