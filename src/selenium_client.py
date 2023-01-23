from selenium.webdriver import ChromeOptions, Remote
from selenium.webdriver.remote.webdriver import WebDriver


def start_chrome_driver() -> WebDriver:
    chrome_options = ChromeOptions()
    chrome_options_arguments = [
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--incognito",
        "--disable-dev-shm-usage",
        "--disable-application-cache",
        "--disable-extensions",
    ]
    for argument in chrome_options_arguments:
        chrome_options.add_argument(argument)

    return Remote(
        command_executor="http://web_scraper_denca_2-selenium:4444/wd/hub",
        options=chrome_options
    )
