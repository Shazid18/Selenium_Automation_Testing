from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SEOTests:
    def __init__(self, driver, excel_handler, url_checker):
        self.driver = driver
        self.excel_handler = excel_handler
        self.url_checker = url_checker
        self.base_url = "https://www.alojamiento.io/property/charming-apartment-in-awesome-sevilla-with-ac-wifi/HA-61511677097"

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

        # Initialize status and error messages
        status = "pass"
        error_messages = []

        # Check for sequence starting from h1
        max_level_found = 0
        for i in range(1, 7):
            if heading_counts[f"h{i}"] > 0:
                max_level_found = i

        # Check for missing tags in sequence up to max_level_found
        missing_tags = []
        for i in range(1, max_level_found + 1):
            if heading_counts[f"h{i}"] == 0:
                missing_tags.append(f"h{i}")
                status = "fail"

        if missing_tags:
            error_messages.append(f"Missing heading tags: {', '.join(missing_tags)}")

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
        for i in range(len(all_headings) - 1):
            current_level = all_headings[i]['level']
            next_level = all_headings[i + 1]['level']
            
            # If next level jumps by more than 1, it's a sequence break
            if next_level - current_level > 1:
                status = "fail"
                error_messages.append(
                    f"Sequence break: {all_headings[i]['tag']} ('{all_headings[i]['content']}') "
                    f"followed by {all_headings[i + 1]['tag']} ('{all_headings[i + 1]['content']}')"
                )
            # If next level goes backwards by more than the current level, it's a sequence break
            elif next_level < current_level and next_level != 1:  # Allow h1 to appear after any level
                status = "fail"
                error_messages.append(
                    f"Invalid sequence: {all_headings[i]['tag']} ('{all_headings[i]['content']}') "
                    f"followed by {all_headings[i + 1]['tag']} ('{all_headings[i + 1]['content']}')"
                )

        # Prepare comments
        if status == "pass":
            comments = "All heading tags are in correct sequence"
        else:
            comments = " | ".join(error_messages)

        # Add the heading counts to comments
        comments += " | Heading counts: " + ", ".join(
            f"{tag}: {count}" for tag, count in heading_counts.items() if count > 0
        )

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