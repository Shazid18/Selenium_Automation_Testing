import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def test_setup():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    
    # Set up Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Test with a simple webpage
    driver.get("https://www.google.com")
    print(f"Title: {driver.title}")
    time.sleep(2)
    
    # Close the browser
    driver.quit()

if __name__ == "__main__":
    test_setup()