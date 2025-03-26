import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from test_Login import WebDriverExample, test_login  # Import WebDriver wrapper
from Global_Key import CRM_file_path


class CRMHandler(WebDriverExample):
    """Handles CRM Data operations like navigation and data entry."""
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
    def wait_for_overlay_to_disappear(self):
        """Wait for any overlay or modal to disappear."""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.XPATH, "//div[@class='overlay-class']"))  # Replace with actual overlay class
            )
        except:
            pass  # If no overlay is found, continue with the next steps

    def navigate_to_crm_data(self):
        """Navigate to the CRM Data page after login."""
        crm_page = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='CRM Data']"))
        )

        # Scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView();", crm_page)
        time.sleep(5)  # Give time for animation to complete

        # Click using JavaScript if normal click fails
        try:
            crm_page.click()
        except:
            self.driver.execute_script("arguments[0].click();", crm_page)

        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//h1[normalize-space()='CRM Data']"))
        # )

    def add_crm_data(self):
        """Add new CRM Data."""
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "ngx-overlay"))
        )
        self.wait_for_overlay_to_disappear()  # Wait for overlay to disappear
        add_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add CRM Data']"))
        )
        add_button.click()

        # Generate a unique CRM name
        dynamic_crm_name = f"Test_Crm_Data_{int(time.time())}"
        time.sleep(3)
        crm_name_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "leadCrmName"))
        )
        crm_name_field.send_keys(dynamic_crm_name)

        # Upload file
        file_upload_field = self.driver.find_element(By.XPATH, "//input[@type='file']")
        file_upload_field.send_keys(CRM_file_path)
        time.sleep(3)
        # Click Submit Button
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form//div[text()='Submit']"))
        )
        submit_button.click()
        time.sleep(3)


@pytest.mark.usefixtures("driver")
def test_crm_data_operations(driver):
    """Test CRM Data addition flow with window handling."""
    test_login(driver)  # Ensure login doesn't close the session

    # Ensure the driver has an active window
    if not driver.window_handles:
        pytest.fail("No active browser window found. Test aborted.")

    # If multiple windows exist, switch to the last one
    driver.switch_to.window(driver.window_handles[-1])

    crm_handler = CRMHandler(driver)
    crm_handler.navigate_to_crm_data()
    crm_handler.add_crm_data()