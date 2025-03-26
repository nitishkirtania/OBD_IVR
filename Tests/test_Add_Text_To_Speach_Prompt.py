import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from test_Login import WebDriverExample, test_login


class PromptTextHandler(WebDriverExample):
    """Handles Prompt Text operations like navigation and text entry."""

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def navigate_to_text_to_speech(self):
        """Navigate to the Text to Speech page after login."""
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "ngx-overlay")))

        try:
            prompt_page = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Prompt")))
            prompt_page.click()
        except:
            print("Element click intercepted, forcing click using JavaScript.")
            self.driver.execute_script("arguments[0].click();", prompt_page)

    def add_text_prompt(self):
        """Add new Text Prompt."""
        wait = WebDriverWait(self.driver, 10)

        try:
            add_prompt_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add Prompt']"))
            )
            self.driver.execute_script("arguments[0].click();", add_prompt_button)
            print("Button clicked successfully.")
        except Exception as e:
            pytest.fail(f"Failed to click the 'Add Prompt' button: {e}")

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "ngx-overlay"))
        )

        text_prompt_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Text Prompt']"))
        )
        text_prompt_link.click()
        time.sleep(5)

        timestamp = time.strftime("%Y%m%d%H%M%S")
        dynamic_recording_name = f"Recording_{timestamp}"
        print(f"Generated dynamic name: {dynamic_recording_name}")

        recording_name_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Recording name']"))
        )
        recording_name_field.send_keys(dynamic_recording_name)
        time.sleep(5)

        tts_recording_field = self.driver.find_element(By.XPATH, "//textarea[@placeholder='TTS Recording']")
        tts_recording_field.send_keys("Hello how are you")
        time.sleep(3)

        submit_button = self.driver.find_element(By.XPATH, "//button[normalize-space()='Submit']")
        submit_button.click()
        time.sleep(5)


@pytest.mark.usefixtures("driver")
def test_prompt_text_operations(driver):
    """Test Prompt Text addition flow with window handling."""
    test_login(driver)

    if not driver.window_handles:
        pytest.fail("No active browser window found. Test aborted.")

    driver.switch_to.window(driver.window_handles[-1])

    prompt_text_handler = PromptTextHandler(driver)
    prompt_text_handler.navigate_to_text_to_speech()
    prompt_text_handler.add_text_prompt()
