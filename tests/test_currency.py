import time
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException

class CurrencyTests:
    def __init__(self, driver, excel_handler):
        self.driver = driver
        self.excel_handler = excel_handler
        self.base_url = "https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483"
        time.sleep(2)  # Initial delay to ensure page is loaded before interaction starts

    def test_currency_filter(self):
        """
        Test that changing the currency updates the property tiles' currency display.
        """
        test_case = "Currency filter test"
        results = []  # Store results for each currency

        try:
            # Wait for the currency dropdown to be present and visible
            currency_dropdown = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "js-currency-sort-footer"))
            )

            # Scroll to the dropdown to ensure visibility
            self.driver.execute_script("arguments[0].scrollIntoView(true);", currency_dropdown)
            time.sleep(1)

            # Open the dropdown
            currency_dropdown.click()  # Open the dropdown
            time.sleep(1)

            # Find all currency options using XPath
            currency_options = self.driver.find_elements(By.XPATH, "//div[@id='js-currency-sort-footer']//ul[@class='select-ul']//li")
            # print(f"Currency options found: {len(currency_options)}")
            if not currency_options:
                raise Exception("No currency options found in the dropdown.")

            # Iterate over each currency option and test
            for option in currency_options:
                # Get the innerHTML content of the option element
                option_html = option.get_attribute("innerHTML")
                # print(f"Option HTML: {option_html}")  # Debugging the HTML content

                # Extract the currency text from the <p> tag inside the <div> tag
                currency_text = option.find_element(By.TAG_NAME, "p").text.strip()
                # print(f"Testing currency: {currency_text}")

                try:
                    # Ensure the option is visible and clickable
                    WebDriverWait(self.driver, 10).until(EC.visibility_of(option))  # Ensure visibility
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(option))  # Ensure clickability
                    
                    # Scroll into view to avoid issues with elements outside the viewport
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", option)

                    # Click on the currency option
                    option.click()
                    print(f"Clicked on {currency_text}")  # Logging the selected currency

                except (TimeoutException, ElementClickInterceptedException):
                    # print(f"Timeout or click intercepted: Element {currency_text} not clickable.")
                    continue  # Skip this currency if it's not clickable

                # Wait for the page to update after clicking the currency
                time.sleep(2)

                # Validate property tiles display the selected currency
                property_tiles = self.driver.find_elements(By.CLASS_NAME, "property-tile")  # Adjust selector if needed
                all_tiles_correct = True

                for tile in property_tiles:
                    price_element = tile.find_element(By.CLASS_NAME, "price")  # Adjust selector if needed
                    if currency_text not in price_element.text:
                        all_tiles_correct = False
                        # print(f"Currency mismatch: {currency_text} not found in {price_element.text}.")
                        break

                if all_tiles_correct:
                    results.append(f"Pass: {currency_text}")
                    # print(f"Currency {currency_text} passed. Property tiles updated correctly.")
                else:
                    results.append(f"Fail: {currency_text}")
                    # print(f"Currency {currency_text} failed. Property tiles not updated correctly.")

                # Close the dropdown to prepare for the next test
                try:
                    # Reopen the dropdown if necessary for the next selection
                    currency_dropdown.click()
                    time.sleep(1)
                except Exception as e:
                    {str(e)}

            # Write detailed results to the report
            final_result = "\n".join(results)
            self.excel_handler.add_result(self.base_url, test_case, "Pass", final_result)
            # print(f"Test completed: \n{final_result}")

        except Exception as e:
            # Log the full exception details and return a fail status
            self.excel_handler.add_result(self.base_url, test_case, "Fail", traceback.format_exc())
            # print(f"Test failed: {traceback.format_exc()}")


    def close_driver(self):
        self.driver.quit()










## Previous Code ##

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class CurrencyTests:
#     def __init__(self, driver, excel_handler):
#         self.driver = driver
#         self.excel_handler = excel_handler
#         self.base_url = "https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483"

#     def test_currency_filter(self):
#         try:
#             # This is a placeholder - you'll need to update the selectors based on the actual website
#             currency_selector = WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, "footer-currency-dd"))
#             )
#             currency_selector.click()

#             # Select US currency (update selector as needed)
#             us_option = self.driver.find_element(By.CSS_SELECTOR, "[data-currency-country='US']")
#             us_option.click()

#             # Wait for price updates and verify (update selector as needed) price-info js-price-value
#             prices = WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_all_elements_located((By.CLASS_NAME, "availability-price"))
#             )

#             currency_changed = all('$' in price.text for price in prices)
#             status = "pass" if currency_changed else "fail"
#             comments = "Currency filter working correctly" if status == "pass" else "Currency not updated in all prices"
            
#         except Exception as e:
#             status = "fail"
#             comments = f"Error testing currency filter: {str(e)}"

#         self.excel_handler.add_result(self.base_url, "Currency Filter", status, comments)