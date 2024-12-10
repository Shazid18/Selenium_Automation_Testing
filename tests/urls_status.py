import requests
from selenium.webdriver.common.by import By

class URLsStatusTest:
    def __init__(self, driver, excel_handler, url_checker, base_url):
        self.driver = driver
        self.excel_handler = excel_handler
        self.url_checker = url_checker
        self.base_url = base_url

    def run(self):
        total_links = 0
        broken_links = []
        
        # Find all 'a' tags
        links = self.driver.find_elements(By.TAG_NAME, "a")
        total_links = len(links)
        
        # Check each link
        for link in links:
            try:
                url = link.get_attribute('href')
                # Ensure url is valid and not a javascript, mailto, or tel link
                if url and not url.startswith(('javascript:', 'mailto:', 'tel:')):
                    response = requests.head(url, allow_redirects=True, timeout=5)
                    if response.status_code == 404:
                        broken_links.append({
                            'url': url,
                            'status_code': response.status_code,
                            'text': link.text.strip() or 'No link text'
                        })
            except requests.RequestException as e:
                broken_links.append({
                    'url': url if 'url' in locals() else 'Unknown URL',
                    'status_code': 'Error',
                    'text': link.text.strip() or 'No link text',
                    'error': str(e)  # Log the error details
                })
        
        # Determine pass or fail status
        status = "pass" if not broken_links else "fail"
        
        # Prepare the comment section
        if status == "pass":
            comments = f"All {total_links} links are working properly"
        else:
            broken_links_details = []
            for link in broken_links:
                if link['status_code'] == 'Error':
                    detail = f"URL: {link['url']} | Text: '{link['text']}' | Error: {link['error']}"
                else:
                    detail = f"URL: {link['url']} | Text: '{link['text']}' | Status Code: {link['status_code']}"
                broken_links_details.append(detail)
            
            comments = f"Found {len(broken_links)} broken links out of {total_links} total links\n" + "\n".join(broken_links_details)

        # Log the results to Excel
        self.excel_handler.add_result(self.base_url, "URLs Status", status, comments)
