from selenium.webdriver.common.by import By

class HeadingSequenceTest:
    def __init__(self, driver, excel_handler, url_checker, base_url):
        self.driver = driver
        self.excel_handler = excel_handler
        self.url_checker = url_checker
        self.base_url = base_url

    def run(self):
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
