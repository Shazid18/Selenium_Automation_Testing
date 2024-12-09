from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CurrencyTests:
    def __init__(self, driver, excel_handler):
        self.driver = driver
        self.excel_handler = excel_handler
        self.base_url = "https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483"

    def test_currency_filter(self):
        try:
            # This is a placeholder - you'll need to update the selectors based on the actual website
            currency_selector = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "footer-currency-dd"))
            )
            currency_selector.click()

            # Select US currency (update selector as needed)
            us_option = self.driver.find_element(By.CSS_SELECTOR, "[data-currency-country='US']")
            us_option.click()

            # Wait for price updates and verify (update selector as needed) price-info js-price-value
            prices = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "availability-price"))
            )

            currency_changed = all('$' in price.text for price in prices)
            status = "pass" if currency_changed else "fail"
            comments = "Currency filter working correctly" if status == "pass" else "Currency not updated in all prices"
            
        except Exception as e:
            status = "fail"
            comments = f"Error testing currency filter: {str(e)}"

        self.excel_handler.add_result(self.base_url, "Currency Filter", status, comments)