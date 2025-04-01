import pytest
import os
import time
import pandas as pd
import glob
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_Login import WebDriverExample, test_login


class test_ReportCampaignWise(WebDriverExample):
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

        try:
            # Ensure the element is visible and clickable
            campaign_wise = waits.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//label[@for='mat-radio-3-input']//div[@class='mat-radio-inner-circle']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", campaign_wise)
            time.sleep(2)  # Give time for the page to adjust
            campaign_wise.click()
            print("✅ Campaign-wise report selected.")
        except Exception as e:
            pytest.fail(f"❌ Error selecting campaign-wise report: {e}")

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
        rows = self.driver.find_elements(By.XPATH, "//table[@id='campaignSummaryTable']//thead[@class='thead-dark']//tr")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 12:  # Ensure the row has enough columns
                execution_date = cells[1].text.strip()
                user_name = cells[2].text.strip()
                campaign_name = cells[3].text.strip()
                total_msisdn = int(cells[4].text.strip().replace(",", ""))  # Remove commas
                valid_msisdn = int(cells[5].text.strip().replace(",", ""))
                attempted_calls = int(cells[6].text.strip().replace(",", ""))
                connected_calls = int(cells[7].text.strip().replace(",", ""))
                digit_pressed = int(cells[8].text.strip())
                listen_rate = cells[9].text.strip()
                total_bill_sec = int(cells[10].text.strip().replace(",", ""))
                credits_used = int(cells[11].text.strip().replace(",", ""))
                call_patch = int(cells[12].text.strip())
                user_data[user_name] = {
                    "execution_date": execution_date,
                    "campaign_name": campaign_name,
                    "total_msisdn": total_msisdn,
                    "valid_msisdn": valid_msisdn,
                    "attempted_calls": attempted_calls,
                    "connected_calls": connected_calls,
                    "digit_pressed": digit_pressed,
                    "listen_rate": listen_rate,
                    "total_bill_sec": total_bill_sec,
                    "credits_used": credits_used,
                    "call_patch": call_patch
                }

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
                files = sorted(glob.glob(os.path.join(download_dir, "CampaignSummary_*.csv")), key=os.path.getmtime,
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
                user_name = row["user name"].strip()
                csv_data[user_name] = {
                    "execution_date": row["execution date"].strip(),
                    "campaign_name": row["campaign name"].strip(),
                    "total_msisdn": int(str(row["total msisdn"]).strip().replace(",", "")),
                    "valid_msisdn": int(str(row["valid msisdn"]).strip().replace(",", "")),
                    "attempted_calls": int(str(row["attempted calls"]).strip().replace(",", "")),
                    "connected_calls": int(str(row["connected calls"]).strip().replace(",", "")),
                    "digit_pressed": int(str(row["digit pressed"]).strip()),
                    "listen_rate": row["listen rate"].strip(),
                    "total_bill_sec": int(str(row["total bill sec"]).strip().replace(",", "")),
                    "credits_used": int(str(row["credits used"]).strip().replace(",", "")),
                    "call_patch": int(str(row["call patch"]).strip())
                }

            print("✅ Extracted CSV Data:", csv_data)

        #     # Validate against extracted web data
        #     assert csv_data == web_data, "❌ Mismatch between web data and CSV data!"
        #     print("✅ Data Matched Successfully!")
        #
        # except Exception as e:
        #     pytest.fail(f"❌ Error validating CSV file: {e}")
            # Compare CSV data with extracted web data
            mismatches = []
            for user, csv_entry in csv_data.items():
                if user not in web_data:
                    mismatches.append(f"❌ User {user} not found in web data")
                    continue

                web_entry = web_data[user]
                for key in csv_entry:
                    if csv_entry[key] != web_entry[key]:
                        mismatches.append(
                            f"❌ Mismatch for {user} in {key}: Web({web_entry[key]}) vs CSV({csv_entry[key]})")

            if mismatches:
                pytest.fail("\n".join(mismatches))
            else:
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
    report_handler = test_ReportCampaignWise(driver)
    report_handler.navigate_to_report_page()
    web_data = report_handler.extract_table_data()

    # Define download directory
    download_dir = os.path.expanduser("~/Downloads")

    csv_file = report_handler.download_report(download_dir)
    report_handler.validate_csv_with_web_data(csv_file, web_data)

    print("✅ Test completed successfully!")
