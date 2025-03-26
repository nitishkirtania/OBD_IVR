import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from test_Login import WebDriverExample, test_login
from Global_Key import Add_Dynamic_TTS_datafile


class CampaignHandler(WebDriverExample):
    """Handles Campaign operations like navigation and form filling."""

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def navigate_to_campaign_page(self):
        """Navigate to the Campaign page after login."""
        WebDriverWait(self.driver, 15).until(lambda d: len(d.window_handles) > 0)
        print(f"Available Windows after login: {self.driver.window_handles}")

        waits = WebDriverWait(self.driver, 15)
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        try:
            add_campaign_button = waits.until(
                EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='Campaign']")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_campaign_button)
            time.sleep(2)  # Allow animation to complete
            add_campaign_button.click()
            print("Navigated to Campaign page.")
        except Exception as e:
            pytest.fail(f"Error clicking Campaign button: {e}")

    def add_campaign_responsive(self):
        """Click on 'Add Campaign' button using JavaScript."""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "ngx-overlay"))
            )
            add_campaign_button = self.driver.find_element(By.XPATH, "//button[normalize-space()='Add Campaign']")
            self.driver.execute_script("arguments[0].click();", add_campaign_button)
            print("Campaign button clicked using JavaScript.")
        except Exception as e:
            pytest.fail(f"Error in add_campaign_responsive: {e}")

    def fill_campaign_details(self):
        """Fill out campaign details and submit the form."""
        dynamic_campaign_name = "Test_Camp_" + str(int(time.time()))
        campaign_name_input = self.driver.find_element(By.XPATH, "//input[@id='mat-input-4']")
        campaign_name_input.send_keys(dynamic_campaign_name)

        try:
            WebDriverWait(self.driver, 15).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "ngx-overlay"))
            )
            camp_type_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='col-12 col-xl-4 mb-4 mb-xl-0']//div[@class='row']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", camp_type_dropdown)
            camp_type_dropdown.click()
            Dynamic_TTS_Campaign_select = self.driver.find_element(By.XPATH, "//span[normalize-space()='Dynamic TTS']")
            Dynamic_TTS_Campaign_select.click()
        except Exception as e:
            pytest.fail(f"Error clicking campaign type dropdown: {e}")

        time.sleep(5)
        gender_button = self.driver.find_element(By.XPATH, "//label[@for='mat-radio-20-input']//div[@class='mat-radio-outer-circle']")
        gender_button.click()

        language_list = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//mat-select[@id='mat-select-9']//div[@class='mat-select-arrow-wrapper']"))
        )
        language_list.click()
        option = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Telugu']"))
        )
        option.click()

        tts_record_field = self.driver.find_element(By.XPATH, "//textarea[@placeholder='TTS Recording']")
        tts_record_field.send_keys("Hello, how are you is there any thing new {Name}")

        click_submit = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='label']"))
        )
        click_submit.click()

        upload_file_csv = self.driver.find_element(By.XPATH, "//input[@type='file']")
        upload_file_csv.send_keys(Add_Dynamic_TTS_datafile)
        time.sleep(10)
        enter_testing_number = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='file-upload-wrapper'] input[type='file']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", enter_testing_number)
        enter_testing_number.send_keys(Add_Dynamic_TTS_datafile)

        click_to_test_call = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Test Campaign']"))
        )
        self.driver.execute_script("arguments[0].click();", click_to_test_call)

        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit']"))
        )
        self.driver.execute_script("arguments[0].click();", submit_button)

        click_ok_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Ok']"))
        )
        self.driver.execute_script("arguments[0].click();", click_ok_button)


@pytest.mark.usefixtures("driver")
def test_campaign_operations(driver):
    """Test Campaign creation flow with window handling."""
    test_login(driver)

    if not driver.window_handles:
        pytest.fail("No active browser window found. Test aborted.")

    print(f"Available Windows before switching: {driver.window_handles}")
    driver.switch_to.window(driver.window_handles[-1])

    campaign_handler = CampaignHandler(driver)
    campaign_handler.navigate_to_campaign_page()
    campaign_handler.add_campaign_responsive()
    campaign_handler.fill_campaign_details()
