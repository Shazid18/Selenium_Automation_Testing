# Vacation Rental Home Page Automation Testing

 ## Table of Contents
  
  1. [Project Overview](#project-overview)
  2. [Features](#features)
  3. [Project Structure](#project-structure)
  4. [Getting Started](#getting-started)
     - [Prerequisites](#prerequisites)
     - [Dependencies](#dependencies)
     - [Installation](#installation)
  6. [Usage](#usage)
  7. [Reusability of Code](#reusability-of-code)

## Project Overview

This project is designed to automate the testing of a vacation rental details page to validate essential elements and functionality. The tests ensure that the webpage meets SEO and functional standards.




## Features

- **H1 tag existence**: Checks if the H1 tag is present on the page.

- **HTML tag sequence**: Ensure proper order of H1-H6 tags and also in correctly sequenced.

- **Image alt attribute**: Validates that all images have proper alt attributes for SEO purposes.

- **URL status code**: Verifies the HTTP status of all URLs on the page to ensure there are no broken links. (i.e., not 404).

- **Currency filter functionality**: Verify that currency changes on the page update the property tiles accordingly.

- **Script data extraction**: Extract critical site information (like SiteURL, CampaignID, etc.) and record it into an Excel file.

The results of each test are recorded in an Excel file with detailed comments on pass/fail criteria.


## Project Structure
  
  ```plaintext

     Selenium/
      ├── config/
      │   └── config.py               # Configuration settings (e.g., URLs, credentials)
      ├── tests/
      │   ├── __init__.py             # Makes 'tests' a package
      │   ├── h1_existence.py         # Checks for the presence of <h1> tags
      │   ├── heading_sequence.py     # Verifies the sequence of headings
      │   ├── image_alt_attributes.py # Tests for missing or empty alt attributes in images
      │   ├── scrape_data.py          # Scrapes data from pages
      │   ├── test_currency.py        # Tests currency functionality
      │   └── urls_status.py          # Verifies the status of URLs
      ├── utils/
      │   ├── __init__.py             # Makes 'utils' a package
      │   ├── driver_setup.py         # WebDriver setup and initialization
      │   ├── excel_handler.py        # Handles Excel file operations
      │   └── url_checker.py          # Utility for checking URL statuses
      ├── .gitignore                  # Specifies files and directories to ignore in Git
      ├── README.md                   # Project documentation
      ├── automation_report.xlsx      # Output file for test results
      ├── main.py                     # Entry point for executing tests
      ├── requirements.txt            # Python dependencies for the project
      ├── script_data.xlsx            # Input data for tests (if any)
      └── test.py                     # Script for running or debugging specific tests

  ```




  ## Getting Started
  
### Prerequisites

1. **Python**  
   - Version >= 3.8  
   - [Download Python](https://www.python.org/downloads/)

2. **Browser**  
   - Google Chrome or Mozilla Firefox must be installed. (Chrome recommended) 
   - [Download Google Chrome](https://www.google.com/chrome/)  
   - [Download Firefox](https://www.mozilla.org/firefox/)

3. **WebDriver Manager**
    - The project uses the `webdriver_manager` library to automatically download and manage the appropriate WebDriver version, so no manual WebDriver installation is required.


### Dependencies

This project requires the following Python packages:

- **selenium**: For browser automation.
- **pandas**: For Excel report generation.
- **openpyxl**: For writing to Excel files.
- **requests**: For handling HTTP requests.
- **webdriver-manager**: For automatically managing WebDriver installations.

### Installation
  
  1. Clone the repository:
     ```bash
     git clone https://github.com/Shazid18/Selenium_V1.git
     cd Selenium_V1
     ```
  
  2. Set up a virtual environment:
     ```bash
     python3 -m venv venv
     ```
     
  3. Activate the virtual environment:
     ```bash
     source venv/bin/activate   # On Windows: venv\Scripts\activate
     ```
  
  4. Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```


## Usage

### Set up the configuration:
- Make sure `config/config.py` contains the correct settings for your ChromeDriver and other configuration options.

- To change the test webpage, simply change the BASE_URL in the `config/config.py` file. (Currently set to the vacation rental page)

- By default, the project uses `webdriver-manager` to download the correct version of ChromeDriver automatically. However, if you want to manually specify the driver path, set `USE_CHROMEDRIVER_MANAGER = False` in `config/config.py`.

### Running the tests:
- You can run the tests using the main.py script. This script will automatically:
     - Set up the Selenium WebDriver.
     - Run the tests for h1 tag existence, html tag sequence, image alt attribute validation, URLs check, currency filter, and data extraction.
     - Store the results in an Excel report.

     To run the tests, execute:
     ```bash
     python main.py 
     ```
### Test Results:
- The results are stored in `automation_report.xlsx`. Each test writes its results to a separate sheet in the same Excel file. The file will include detailed information about each test, such as the tested page url, test case name, pass/fail status and comments.

### Scrape data from Script data: 
- Extracts important information such as Site URL, Campaign ID, SiteName, Browser, CountryCode and IP from the page and stored in `script_data.xlsx` file.

## Reusability of Code

Code is divided into smaller modules (`config/`, `utils/` and `tests/`) based on their responsibilities. Modules can be reused independently in new projects or extended without affecting unrelated code.

### `config/config.py`
Contains configuration for the browser options, WebDriver, Base_URL (tested url path) and other settings.

### `tests/`
Contains individual test scripts:

- **SEO Tests**:
    - `h1_existence.py`: Tests the existence of `<h1>` tags on the website.
    - `heading_sequence.py`: Validates the correct order of heading tags.
    - `image_alt_attributes.py`: Ensures that images have appropriate alt attributes.
    - `urls_status.py`: Checks the status of URLs on the website.
  
- **Currency Filter Test**:
    - `test_currency.py`: Tests whether the currency filter works as expected on the website.

- **Scrape Data**:
    - `scrape_data.py`: Extracts data (like Site URL, Campaign ID, etc.) and stores it in an Excel file.

### `utils/`
Contains utility modules: Encapsulates the WebDriver setup, making it reusable across all test scripts and handles Excel report generation in a reusable way.

- `driver_setup.py`: Sets up the Selenium WebDriver.
- `excel_handler.py`: Handles reading and writing data to Excel files.
- `url_checker.py`: Validates the URLs on the site.

### `main.py`
This is the main script that ties everything together and runs the tests.