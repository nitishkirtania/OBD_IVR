import pytest
import os
import time
import pandas as pd
import glob
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_Login import WebDriverExample, test_login


class test_Report(WebDriverExample):
    """Handles Report operations like navigation, data extraction, and file validation."""

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def navigate_to_report_page(self):
        """Navigate to the Report page after login."""
        WebDriverWait(self.driver, 15).until(lambda d: len(d.window_handles) > 0)
        print(f"Available Windows after login: {self.driver.window_handles}")

        waits = WebDriverWait(self.driver, 15)
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        try:
            report_button = waits.until(
                EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='Report']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", report_button)
            time.sleep(2)  # Allow animation to complete
            report_button.click()
            print("✅ Navigated to Report page.")
        except Exception as e:
            pytest.fail(f"❌ Error clicking Report button: {e}")

    def extract_table_data(self):
        """Extracts data from the web table before downloading the report."""
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "ngx-overlay"))
        )

        search_button = self.driver.find_element(By.XPATH, "//button[normalize-space()='Search']")
        self.driver.execute_script("arguments[0].click();", search_button)
        print("✅ User Report button clicked using JavaScript.")

        time.sleep(5)  # Allow table to load

        user_data = {}
        rows = self.driver.find_elements(By.XPATH, "//table[@id='userSummaryTable']/tbody/tr")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 3:  # Ensure the row has enough columns
                user_name = cells[2].text.strip()
                total_msisdn = int(cells[3].text.strip().replace(",", ""))  # Remove commas
                user_data[user_name] = total_msisdn

        print("✅ Extracted Web Table Data:", user_data)
        return user_data

    def download_report(self, download_dir):
        """Clicks the Export button and waits for the correct file to download."""
        waits = WebDriverWait(self.driver, 20)

        try:
            # Wait for Export Button to be Clickable
            export_button = waits.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Export File']")))

            # Record the timestamp before clicking
            pre_download_time = time.time()

            self.driver.execute_script("arguments[0].click();", export_button)
            print("✅ Export button clicked.")
            time.sleep(5)  # Give time for download to start

            timeout = 60  # Increased timeout for larger reports
            start_time = time.time()
            downloaded_file = None

            print("⏳ Waiting for file download...")

            while time.time() - start_time < timeout:
                # Get all matching UserSummary_*.csv files
                files = sorted(glob.glob(os.path.join(download_dir, "UserSummary_*.csv")), key=os.path.getmtime,
                               reverse=True)

                for file in files:
                    file_time = os.path.getmtime(file)  # Get file modification time
                    if file_time > pre_download_time:  # Ensure file was created after clicking Export
                        downloaded_file = file
                        print(f"✅ Correct downloaded file found: {downloaded_file}")
                        break

                if downloaded_file:
                    break

                time.sleep(2)  # Retry every 2 seconds

            if not downloaded_file:
                pytest.fail("❌ CSV file was not downloaded within the timeout period.")

            return downloaded_file

        except Exception as e:
            pytest.fail(f"❌ Error downloading report: {e}")

    def validate_csv_with_web_data(self, csv_file, web_data):
        """Compares downloaded CSV file data with extracted web data."""
        try:
            df = pd.read_csv(csv_file)
            print("✅ CSV file contents:")
            print(df.head())  # Show first 5 rows

            # Convert column names to lowercase
            df.columns = df.columns.str.lower().str.strip()

            # Adjust column name references
            csv_data = {}
            for _, row in df.iterrows():
                csv_data[row["user_name"].strip()] = int(str(row["total_msisdn"]).strip().replace(",", ""))

            print("✅ Extracted CSV Data:", csv_data)

            # Validate against extracted web data
            assert csv_data == web_data, "❌ Mismatch between web data and CSV data!"
            print("✅ Data Matched Successfully!")

        except Exception as e:
            pytest.fail(f"❌ Error validating CSV file: {e}")


@pytest.mark.usefixtures("driver")
def test_report_operations(driver):
    """Test report generation and validation."""
    test_login(driver)  # This should already initialize and provide the driver

    if not driver.window_handles:
        pytest.fail("❌ No active browser window found. Test aborted.")

    driver.switch_to.window(driver.window_handles[-1])

    # Use existing WebDriver instead of initializing a new one
    report_handler = test_Report(driver)
    report_handler.navigate_to_report_page()
    web_data = report_handler.extract_table_data()

    # Define download directory
    download_dir = os.path.expanduser("~/Downloads")

    csv_file = report_handler.download_report(download_dir)
    report_handler.validate_csv_with_web_data(csv_file, web_data)

    print("✅ Test completed successfully!")
