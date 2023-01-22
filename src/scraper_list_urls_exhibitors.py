import time
from bs4 import BeautifulSoup

from selenium_driver import start_chrome_driver


def get_detail_urls_from_exhibitor_list(exhibitor_list_url):
    print("Launching Selenium driver")
    selenium_driver = start_chrome_driver()
    time.sleep(5)  # Allow 5 seconds for setup Selenium driver.

    print("Getting exhibitor list page html")
    selenium_driver.get("https://connections.arabhealthonline.com/widget/event/arab-health-2023-2/exhibitors/RXZlbnRWaWV3XzQyMTQ2Nw==")
    time.sleep(5)  # Allow 2 seconds for the web page to open.

    soup = BeautifulSoup(selenium_driver.page_source, "html.parser")
    print(soup)