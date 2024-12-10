from selenium.webdriver.common.by import By

class H1ExistenceTest:
    def __init__(self, driver, excel_handler, url_checker, base_url):
        self.driver = driver
        self.excel_handler = excel_handler
        self.url_checker = url_checker
        self.base_url = base_url

    def run(self):
        h1_tags = self.driver.find_elements(By.TAG_NAME, "h1")
        status = "pass" if len(h1_tags) > 0 else "fail"
        comments = f"Found {len(h1_tags)} H1 tags" if status == "pass" else "No H1 tags found"
        self.excel_handler.add_result(self.base_url, "H1 Tag Existence", status, comments)
