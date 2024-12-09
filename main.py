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
        # Extract ScriptData from JavaScript context
        script_data = driver.execute_script("return window.ScriptData")
        
        # Extract required data
        data = {
            'SiteURL': script_data['config']['SiteUrl'],
            'CampaignID': script_data['pageData']['CampaignId'],
            'SiteName': script_data['config']['SiteName'],
            'Browser': script_data['userInfo']['Browser'],
            'CountryCode': script_data['userInfo']['CountryCode'],
            'IP': script_data['userInfo']['IP'],
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
        driver.get("https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483")

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