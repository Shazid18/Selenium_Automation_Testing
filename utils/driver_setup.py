from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.config import CHROME_OPTIONS, HEADLESS_MODE, HEADLESS_OPTIONS, USE_CHROMEDRIVER_MANAGER, CHROME_DRIVER_PATH

class DriverSetup:
    @staticmethod
    def get_driver():
        chrome_options = Options()
        
        # Add options from config
        for option in CHROME_OPTIONS:
            chrome_options.add_argument(option)

        # Add headless mode if enabled in config
        if HEADLESS_MODE:
            for option in HEADLESS_OPTIONS:
                chrome_options.add_argument(option)
        
        if USE_CHROMEDRIVER_MANAGER:
            # Use ChromeDriverManager to install and manage ChromeDriver
            service = Service(ChromeDriverManager().install())
        else:
            # Use a locally specified chromedriver
            service = Service(CHROME_DRIVER_PATH)
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
