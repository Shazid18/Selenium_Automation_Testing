# config.py

# Base URL of the website to be tested
BASE_URL = "https://www.alojamiento.io/property/apartamentos-centro-col%c3%b3n/BC-189483"

# File paths
EXCEL_FILE = "automation_report.xlsx"

# Timeout for HTTP requests in seconds
REQUEST_TIMEOUT = 5  # Timeout for checking URLs

# Driver configuration
CHROME_DRIVER_PATH = "path/to/chromedriver"  # Optional, if not using ChromeDriverManager

# Whether to use ChromeDriverManager or a local chromedriver path
USE_CHROMEDRIVER_MANAGER = True

# WebDriver options
CHROME_OPTIONS = [
    "--start-maximized",
    "--disable-notifications"
]
