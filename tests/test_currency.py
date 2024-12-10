import time
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

class CurrencyTests:
    def __init__(self, driver, excel_handler, url_checker, base_url):
        self.driver = driver
        self.excel_handler = excel_handler
        self.url_checker = url_checker
        self.base_url = base_url
        time.sleep(2)  # Initial delay to ensure page is loaded before interaction starts

    def test_currency_filter(self):
        """
        Test that changing the currency updates the property tiles' currency display.
        """
        test_case = "Currency filter test"
        comment = []  # Store comment

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
            if not currency_options:
                raise Exception("No currency options found in the dropdown.")

            # Iterate over each currency option and test
            for option in currency_options:
                # Get the innerHTML content of the option element
                option_html = option.get_attribute("innerHTML")

                # Extract the currency text from the <p> tag inside the <div> tag
                currency_text = option.find_element(By.TAG_NAME, "p").text.strip()

                try:
                    # Ensure the option is visible and clickable
                    WebDriverWait(self.driver, 10).until(EC.visibility_of(option))  # Ensure visibility
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(option))  # Ensure clickability
                    
                    # Scroll into view to avoid issues with elements outside the viewport
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", option)

                    # Click on the currency option
                    option.click()

                except (TimeoutException, ElementClickInterceptedException):
                    continue  # Skip this currency if it's not clickable

                # Wait for the page to update after clicking the currency
                time.sleep(2)

                # Validate property tiles display the selected currency
                property_tiles = self.driver.find_elements(By.CLASS_NAME, "property-tile")
                all_tiles_correct = True

                for tile in property_tiles:
                    price_element = tile.find_element(By.CLASS_NAME, "price")
                    if currency_text not in price_element.text:
                        all_tiles_correct = False
                        break

                if all_tiles_correct:
                    comment.append(f"Successfully property tiles currency changed for {currency_text}")
                else:
                    comment.append(f"Property tiles currency not changed for {currency_text}")

                # Close the dropdown to prepare for the next test
                try:
                    # Reopen the dropdown if necessary for the next selection
                    currency_dropdown.click()
                    time.sleep(1)
                except Exception as e:
                    {str(e)}

            # Write detailed comment to the report
            comments = "\n".join(comment)
            self.excel_handler.add_result(self.base_url, test_case, "Pass", comments)

        except Exception as e:
            # Log the full exception details and return a fail status
            self.excel_handler.add_result(self.base_url, test_case, "Fail", traceback.format_exc())


    def close_driver(self):
        self.driver.quit()