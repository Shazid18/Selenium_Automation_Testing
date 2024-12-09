import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SEOTests:
    def __init__(self, driver, excel_handler, url_checker):
        self.driver = driver
        self.excel_handler = excel_handler
        self.url_checker = url_checker
        self.base_url = "https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483"

    def test_h1_existence(self):
        h1_tags = self.driver.find_elements(By.TAG_NAME, "h1")
        status = "pass" if len(h1_tags) > 0 else "fail"
        comments = f"Found {len(h1_tags)} H1 tags" if status == "pass" else "No H1 tags found"
        self.excel_handler.add_result(self.base_url, "H1 Tag Existence", status, comments)

    def test_heading_sequence(self):
        # Dictionary to store headings and their counts
        heading_counts = {f"h{i}": 0 for i in range(1, 7)}
        
        # Find and count all heading tags
        for i in range(1, 7):
            tags = self.driver.find_elements(By.TAG_NAME, f"h{i}")
            heading_counts[f"h{i}"] = len(tags)

        # Initialize status
        status = "pass"

        # Check for missing tags (checking all tags from h1 to h6)
        missing_tags = []
        for i in range(1, 7):  # Check all tags from h1 to h6
            if heading_counts[f"h{i}"] == 0:
                missing_tags.append(f"h{i}")
                status = "fail"

        # Get all headings in order of appearance
        all_headings = []
        for tag in self.driver.find_elements(By.XPATH, "//*[self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6]"):
            level = int(tag.tag_name[1])
            all_headings.append({
                'level': level,
                'tag': tag.tag_name,
                'content': tag.text.strip()
            })

        # Check for sequence breaks
        sequence_breaks = []
        for i in range(len(all_headings) - 1):
            current_level = all_headings[i]['level']
            next_level = all_headings[i + 1]['level']
            
            # If next level jumps by more than 1, it's a sequence break
            if next_level - current_level > 1:
                status = "fail"
                sequence_breaks.append(
                    f"Sequence break: {all_headings[i]['tag']} to {all_headings[i + 1]['tag']}"
                )
            # If next level goes backwards by more than the current level, it's a sequence break
            elif next_level < current_level:  # Allow h1 to appear after any level
                status = "fail"
                sequence_breaks.append(
                    f"Invalid sequence: {all_headings[i]['tag']} to {all_headings[i + 1]['tag']}"
                )

        # Prepare comments
        comments = []
        
        # Add missing tags to comments
        if missing_tags:
            comments.append(f"Missing tags: {', '.join(missing_tags)}")
        
        # Add sequence breaks to comments
        if sequence_breaks:
            comments.extend(sequence_breaks)

        # Add heading counts to comments
        heading_count_str = "Heading counts: " + ", ".join(
            f"{tag}: {count}" for tag, count in heading_counts.items() if count > 0
        )
        
        if status == "pass":
            final_comments = "All heading tags are present and in correct sequence | " + heading_count_str
        else:
            final_comments = " | ".join(comments) + " | " + heading_count_str

        self.excel_handler.add_result(self.base_url, "Heading Sequence", status, final_comments)    

    def test_image_alt_attributes(self):
        images = self.driver.find_elements(By.TAG_NAME, "img")
        missing_alt = [img for img in images if not img.get_attribute("alt")]
        
        status = "pass" if not missing_alt else "fail"
        comments = f"All images have alt attributes" if status == "pass" else f"{len(missing_alt)} images missing alt attributes"
        self.excel_handler.add_result(self.base_url, "Image Alt Attributes", status, comments)

    #Checking the url status code
    def test_urls_status(self):
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
                    if response.status_code >= 400:
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
