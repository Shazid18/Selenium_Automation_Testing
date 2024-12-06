from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SEOTests:
    def __init__(self, driver, excel_handler, url_checker):
        self.driver = driver
        self.excel_handler = excel_handler
        self.url_checker = url_checker
        self.base_url = "https://www.alojamiento.io/property/3-springcourt-apartment/BC-2126103"

    def test_h1_existence(self):
        h1_tags = self.driver.find_elements(By.TAG_NAME, "h1")
        status = "pass" if len(h1_tags) > 0 else "fail"
        comments = f"Found {len(h1_tags)} H1 tags" if status == "pass" else "No H1 tags found"
        self.excel_handler.add_result(self.base_url, "H1 Tag Existence", status, comments)

    def test_heading_sequence(self):
        heading_tags = []
        for i in range(1, 7):
            tags = self.driver.find_elements(By.TAG_NAME, f"h{i}")
            if tags:
                heading_tags.append(i)

        is_sequence_valid = True
        for i in range(len(heading_tags)-1):
            if heading_tags[i] > heading_tags[i+1]:
                is_sequence_valid = False
                break

        status = "pass" if is_sequence_valid else "fail"
        comments = "Heading sequence is valid" if status == "pass" else "Invalid heading sequence"
        self.excel_handler.add_result(self.base_url, "Heading Sequence", status, comments)

    def test_image_alt_attributes(self):
        images = self.driver.find_elements(By.TAG_NAME, "img")
        missing_alt = [img for img in images if not img.get_attribute("alt")]
        
        status = "pass" if not missing_alt else "fail"
        comments = f"All images have alt attributes" if status == "pass" else f"{len(missing_alt)} images missing alt attributes"
        self.excel_handler.add_result(self.base_url, "Image Alt Attributes", status, comments)

    def test_urls_status(self):
        links = self.driver.find_elements(By.TAG_NAME, "a")
        broken_links = []
        
        for link in links:
            url = link.get_attribute("href")
            if url and url.startswith(("http", "https")):
                status_code = self.url_checker.check_url_status(self.base_url, url)
                if status_code == 404:
                    broken_links.append(url)

        status = "pass" if not broken_links else "fail"
        comments = "All URLs are valid" if status == "pass" else f"Found {len(broken_links)} broken links"
        self.excel_handler.add_result(self.base_url, "URL Status", status, comments)