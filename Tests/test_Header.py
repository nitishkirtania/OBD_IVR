import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Global_Key import Header_file_path
from test_Login import test_login  # ✅ Explicitly import the driver fixture
from selenium.common.exceptions import ElementClickInterceptedException

class HeaderHandlers:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to_header_page(self):
        """Navigate to the header page."""
        try:
            header_page = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='/header']"))
            )
            self.driver.execute_script("arguments[0].click();", header_page)  # ✅ Click using JS
            print("Navigated to the header page successfully.")

        except ElementClickInterceptedException:
            print("Element click intercepted, trying JavaScript click...")
            self.driver.execute_script("arguments[0].click();", header_page)

        except Exception as e:
            print(f"Error navigating to header page: {str(e)}")
            raise

    def add_header(self):
        """Click to add a new header."""
        try:
            add_header_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='button']"))
            )
            self.driver.execute_script("arguments[0].click();", add_header_button)  # ✅ Click using JS
            print("Clicked 'Add Header' button successfully.")

        except ElementClickInterceptedException:
            print("Element click intercepted, retrying with JavaScript...")
            self.driver.execute_script("arguments[0].click();", add_header_button)

        except Exception as e:
            print(f"Error clicking 'Add Header' button: {str(e)}")
            raise

    def upload_excel_file(self):
        """Upload an Excel file for the header."""
        dynamic_header_name = "Test_Header_" + str(int(time.time()))
        print(f"Using dynamic header name: {dynamic_header_name}")

        # Wait for header name input and enter the name
        header_name_field = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='mat-input-5']"))
        )
        header_name_field.send_keys(dynamic_header_name)
        print("Entered header name successfully.")

        # Wait for file input and upload file using JavaScript (in case it's hidden)
        excel_file_input = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        self.driver.execute_script("arguments[0].style.display = 'block';", excel_file_input)  # Make input visible
        excel_file_input.send_keys(Header_file_path)
        print(f"Uploaded file: {Header_file_path}")
        time.sleep(5)
        # Wait for submit button, scroll into view, and click
        submit_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn.w-50.ml-1"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", submit_button)  # Scroll to button
        time.sleep(1)  # Small delay
        self.driver.execute_script("arguments[0].click();", submit_button)  # Click via JS
        print("Clicked submit button successfully.")
        time.sleep(5)


# ✅ Use the driver fixture
@pytest.mark.usefixtures("driver")
def test_header_operations(driver):
    """Perform header operations after login."""
    test_login(driver)  # ✅ Ensure login happens first
    header_handler = HeaderHandlers(driver)
    header_handler.navigate_to_header_page()
    header_handler.add_header()
    header_handler.upload_excel_file()
