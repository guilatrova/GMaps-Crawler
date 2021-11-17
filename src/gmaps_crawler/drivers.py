from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

IMPLICT_WAIT = 5


def create_driver(headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.implicitly_wait(IMPLICT_WAIT)

    return driver
