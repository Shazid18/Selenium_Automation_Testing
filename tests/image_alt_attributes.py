from selenium.webdriver.common.by import By

class ImageAltAttributesTest:
    def __init__(self, driver, excel_handler, url_checker, base_url):
        self.driver = driver
        self.excel_handler = excel_handler
        self.url_checker = url_checker
        self.base_url = base_url

    def run(self):
        images = self.driver.find_elements(By.TAG_NAME, "img")
        missing_alt = [img for img in images if not img.get_attribute("alt")]
        
        status = "pass" if not missing_alt else "fail"
        comments = f"All images have alt attributes" if status == "pass" else f"{len(missing_alt)} images missing alt attributes"
        self.excel_handler.add_result(self.base_url, "Image Alt Attributes", status, comments)
