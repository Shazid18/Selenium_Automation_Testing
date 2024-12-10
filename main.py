from datetime import datetime
from utils.driver_setup import DriverSetup
from utils.excel_handler import ExcelHandler
from utils.url_checker import URLChecker
from tests.h1_existence import H1ExistenceTest
from tests.heading_sequence import HeadingSequenceTest
from tests.image_alt_attributes import ImageAltAttributesTest
from tests.urls_status import URLsStatusTest
from tests.test_currency import CurrencyTests
from tests.scrape_data import adjust_column_widths, extract_script_data
from config.config import BASE_URL  # Import BASE_URL from config

def main():
    driver = None
    try:
        # Setup the web driver, Excel handler, and URL checker
        driver = DriverSetup.get_driver()
        excel_handler = ExcelHandler()
        url_checker = URLChecker()

        # Navigate to the website using BASE_URL from config
        print(f"Navigating to {BASE_URL}...")
        driver.get(BASE_URL)

        # Run SEO Tests
        print("Running SEO Tests...")
        print("Running H1 Tests...")
        h1_test = H1ExistenceTest(driver, excel_handler, url_checker, driver.current_url)
        h1_test.run()

        print("Running Sequence Tests...")
        heading_test = HeadingSequenceTest(driver, excel_handler, url_checker, driver.current_url)
        heading_test.run()

        print("Running Image alt Tests...")
        image_test = ImageAltAttributesTest(driver, excel_handler, url_checker, driver.current_url)
        image_test.run()

        print("Running URL Tests...")
        url_test = URLsStatusTest(driver, excel_handler, url_checker, driver.current_url)
        url_test.run()

        # Run Currency Tests
        print("Running Currency Tests...")
        currency_tests = CurrencyTests(driver, excel_handler, url_checker, driver.current_url)
        currency_tests.test_currency_filter()

        # Extract Script Data
        print("Extracting Script Data...")
        extract_script_data(driver)

        excel_handler.close()
        print("Test results saved successfully.")

    except Exception as e:
        print(f"Error during test execution: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
