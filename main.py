from datetime import datetime
import pandas as pd
from selenium.webdriver.common.by import By
from utils.driver_setup import DriverSetup
from utils.excel_handler import ExcelHandler
from utils.url_checker import URLChecker
from tests.test_seo import SEOTests
from tests.test_currency import CurrencyTests
import json

def extract_script_data(driver):
    try:
        # This is a placeholder - update the script tag selector based on actual website
        script_element = driver.find_element(By.XPATH, "//script[@type='application/ld+json']")
        script_data = json.loads(script_element.get_attribute('innerHTML'))
        
        # Extract required data (update based on actual script structure)
        data = {
            'SiteURL': driver.current_url,
            'CampaignID': script_data.get('campaignId', ''),
            'SiteName': script_data.get('name', ''),
            'Browser': driver.capabilities['browserName'],
            'CountryCode': script_data.get('countryCode', ''),
            'IP': script_data.get('ip', '')
        }
        
        # Save to Excel
        df = pd.DataFrame([data])
        df.to_excel(f'script_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx', index=False)
        
    except Exception as e:
        print(f"Error extracting script data: {str(e)}")

def main():
    driver = None
    try:
        driver = DriverSetup.get_driver()
        excel_handler = ExcelHandler()
        url_checker = URLChecker()

        # Navigate to the website
        driver.get("https://www.alojamiento.io/property/3-springcourt-apartment/BC-2126103")

        # Run SEO tests
        seo_tests = SEOTests(driver, excel_handler, url_checker)
        seo_tests.test_h1_existence()
        seo_tests.test_heading_sequence()
        seo_tests.test_image_alt_attributes()
        seo_tests.test_urls_status()

        # Run currency tests
        currency_tests = CurrencyTests(driver, excel_handler)
        currency_tests.test_currency_filter()

        # Extract script data
        extract_script_data(driver)

        # Save results
        excel_handler.save_results()

    except Exception as e:
        print(f"Error during test execution: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()