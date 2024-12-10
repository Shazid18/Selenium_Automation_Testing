# Vacation Rental Home Page Automation Testing

## Description

This project is designed to automate the testing of a vacation rental details page to validate essential elements and functionality. The tests ensure that the webpage meets SEO and functional standards. The automation script performs the following:

- **H1 tag existence**: Checks if the H1 tag is present on the page.
- **HTML tag sequence**: Ensure proper order of H1-H6 tags and also in correctly sequenced.
- **Image alt attribute**: Validates that all images have proper alt attributes for SEO purposes.
- **URL status code**: Verifies the HTTP status of all URLs on the page to ensure there are no broken links. (i.e., not 404).
- **Currency filter functionality**: Verify that currency changes on the page update the property tiles accordingly.
- **Script data extraction**: Extract critical site information (like SiteURL, CampaignID, etc.) and record it into an Excel file.

The results of each test are recorded in an Excel file with detailed comments on pass/fail criteria.

 ## Table of Contents
  
  1. [Features](#features)
  2. [Technologies Used](#technologies-used)
  3. [Prerequisites](#prerequisites)
  4. [Project Structure](#project-structure)
  5. [Getting Started](#getting-started)
     - [Installation](#installation)
     - [Database Configuration](#database-configuration)
     - [Running the Application](#running-the-application)
  6. [Usage](#usage)
  7. [Database Schema](#database-schema)
  

## Requirements

### Tools:
- **Python** (Version: 3.x)
- **Selenium** for web automation.
- **Pandas** for generating Excel reports.
- **Requests** for checking URL status codes.

### Browser:
- **Google Chrome** or **Firefox** (make sure to use the corresponding WebDriver version).
- You can download the Chrome WebDriver from [here](https://sites.google.com/chromium.org/driver/), or the Firefox WebDriver from [here](https://github.com/mozilla/geckodriver/releases).

### Test Site URL:
- [https://www.alojamiento.io/property/chic-apartament-retiro-park-i-swimming-pool-elevenhost/BC-5455289](https://www.alojamiento.io/property/chic-apartament-retiro-park-i-swimming-pool-elevenhost/BC-5455289)

### Tests to Perform:
- **H1 Tag Existence Test**: The script will check if the page contains an H1 tag. If missing, the test will fail.
- **HTML Tag Sequence Test**: The script checks that the H1-H6 tags appear in the correct order (H1 before H2, H2 before H3, etc.). If any sequence is broken or missing, the test will fail.
- **Image Alt Attribute Test**: Verifies if all images on the page have an alt attribute. Missing alt attributes will cause the test to fail.
- **URL Status Code Test**: Checks all URLs on the page to ensure they do not return a 404 (Page Not Found) error.
- **Currency Filtering Test**: Tests the property tiles to confirm that their currency changes when a new currency is selected.
- **Script Data Scraping**: Scrapes specific data from the scripts and records it in an Excel file, including:
  - Site URL
  - Campaign ID
  - Site Name
  - Browser
  - Country Code
  - IP address

## Acceptance Criteria

1. **Reusability**: The code and methods should be reusable for different pages or test cases.
2. **Output Format**: The script will generate an excel report for individual test cases.
3. **Report Model**:
   - The report will have the following columns:
     - `page_url`: The URL of the page being tested.
     - `testcase`: The name of the test case.
     - `passed`: Whether the test passed or failed.
     - `comments`: Additional information (such as the status code or missing attributes).


  ## Project Structure
  
  ```plaintext

     Selenium/
     ├── config/
     │   ├── config.py          # Configuration file for driver and browser settings
     ├── tests/
     │   ├── __init__.py        # Empty file to mark the directory as a Python package
     │   ├── h1_existence.py    # SEO test for checking H1 tag existence
     │   ├── heading_sequence.py # SEO test for checking heading order
     │   ├── image_alt_attributes.py # SEO test for checking image alt attributes
     │   ├── scrape_data.py     # Script for extracting data from the page and saving it to Excel
     │   ├── urls_status.py     # SEO test for checking URL status
     │   ├── test_currency.py   # Test for verifying the currency filter functionality
     ├── utils/
     │   ├── driver_setup.py    # Handles WebDriver setup using configurations
     │   ├── excel_handler.py   # Handles reading and writing Excel reports
     │   ├── url_checker.py     # URL validation utilities
     ├── main_test.py           # Main entry point for running the tests
     ├── .gitignore             # Specifies which files should be ignored by Git
     ├── requirements.txt       # List of project dependencies
     ├── script_data.xlsx       # Output file storing extracted data
     └── automation_report.xlsx # Output file storing test results
  ```

## `config/config.py`
Contains configuration for the browser options, WebDriver, and other settings.

## `tests/`
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

## `utils/`
Contains utility modules:

- `driver_setup.py`: Sets up the Selenium WebDriver.
- `excel_handler.py`: Handles reading and writing data to Excel files.
- `url_checker.py`: Validates the URLs on the site.

## `main.py`
This is the main script that ties everything together and runs the tests.


  ## Getting Started
  
  ### Installation
  
  1. Clone the repository:
     ```bash
     git clone https://github.com/your-username/Project_V2_Poe.git
     cd Project_V2_Poe
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
  
### Running the Application


  1. Run All Tests at Once:
     ```bash
     python main.py 
     ```

## Usage

### Set up the configuration:
- Make sure `config/config.py` contains the correct settings for your ChromeDriver and other configuration options.
- By default, the project uses `webdriver-manager` to download the correct version of ChromeDriver automatically. However, if you want to manually specify the driver path, set `USE_CHROMEDRIVER_MANAGER = False` in `config/config.py`.

### Running the tests:
- You can run the tests using the main_test.py script. This script will automatically:
     - Set up the Selenium WebDriver.
     - Run the tests for SEO, currency filter, and data extraction.
     - Store the results in an Excel report.

     To run the tests, execute:
     ```bash
     python main.py 
     ```
### Test Results:
- The results are stored in automation_report.xlsx. The file will include detailed information about each test, such as the pass/fail status and additional messages.

### Scrape data from Script data: 
- Extracts important information such as Site URL, Campaign ID, SiteName, Browser, CountryCode and IP from the page and stored in script_data.xlsx.

### Create a New Branch

```bash
- git checkout -b feature/add-new-feature
```
### Make Modifications and Commit Changes
```bash
- git commit -m 'Add new feature: [brief description of the feature]'

```
### Push Changes to the Branch

```bash
- git push origin feature/add-new-feature

```
### Create a New Pull Request
- Navigate to the repository on GitHub.
- Click on the "Compare & pull request" button.
- Fill in the pull request details and submit it for review.