import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from test_Login import WebDriverExample, test_login
from Global_Key import Lead_data, Select_Lead_campaign_name


class LeadHandler(WebDriverExample):
    """Handles Lead operations like navigation and lead creation."""

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def navigate_to_lead_page(self):
        """Navigate to the Lead page after login."""
        WebDriverWait(self.driver, 15).until(lambda d: len(d.window_handles) > 0)
        print(f"Available Windows after login: {self.driver.window_handles}")

        waits = WebDriverWait(self.driver, 15)
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        try:
            add_lead_button = waits.until(EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='Lead']")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_lead_button)
            time.sleep(2)  # Allow animation to complete
            add_lead_button.click()
            print("Navigated to Lead page.")
        except Exception as e:
            pytest.fail(f"Error clicking Lead button: {e}")

    def add_lead(self):
        """Create a new Lead entry."""
        # Wait for the overlay to disappear
        WebDriverWait(self.driver, 20).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "ngx-overlay"))
        )

        add_lead_button_on = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.create-btn.ml-2"))
        )

        for attempt in range(3):
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", add_lead_button_on)
                time.sleep(1)
                add_lead_button_on.click()
                print("Lead button clicked successfully.")
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(2)

        print("Selecting campaign...")
        campaign_name = self.driver.find_element(By.CLASS_NAME, "mat-select-arrow")
        campaign_name.click()

        try:
            option_to_select = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[normalize-space()='{Select_Lead_campaign_name}']"))
            )
            option_to_select.click()
            time.sleep(3)
            print("Campaign selected: Veer_testin")
        except TimeoutException:
            print("Error: Campaign 'Veer_testin' not found or not clickable.")

        dynamic_lead_name = "Test_Lead_NK_" + str(int(time.time()))
        print(f"Entering lead name: {dynamic_lead_name}")
        wait = WebDriverWait(self.driver, 5)
        enter_lead_name = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Lead name']")))
        enter_lead_name.send_keys(dynamic_lead_name)
        time.sleep(3)

        upload_data = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        upload_data.send_keys(Lead_data)
        time.sleep(5)

        try:
            dnd_uncheck = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[normalize-space()='DND Check']//span[@class='slider round']"))
            )
            dnd_uncheck.click()
            print("DND check disabled.")
        except TimeoutException:
            print("Error: DND Check slider not found.")

        print("Setting cyclic count to 3...")
        cyclic_count = self.driver.find_element(By.XPATH, "//input[@formcontrolname='noOfRetry']")
        cyclic_count.clear()
        cyclic_count.send_keys("3")
        time.sleep(2)

        print("Lead creation process completed. Clicking submit...")
        submit_button_click = self.driver.find_element(By.XPATH, "//button[normalize-space()='Submit']")

        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "ngx-overlay")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button_click)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", submit_button_click)

        print("Clicking OK to finalize lead creation...")
        option_to_OK = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Ok']"))
        )
        self.driver.execute_script("arguments[0].click();", option_to_OK)
        time.sleep(3)

@pytest.mark.usefixtures("driver")
def test_lead_operations(driver):
    """Test Lead creation flow with window handling."""
    test_login(driver)

    if not driver.window_handles:
        pytest.fail("No active browser window found. Test aborted.")

    print(f"Available Windows before switching: {driver.window_handles}")
    driver.switch_to.window(driver.window_handles[-1])

    lead_handler = LeadHandler(driver)
    lead_handler.navigate_to_lead_page()
    lead_handler.add_lead()