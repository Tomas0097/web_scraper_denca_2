import time
from bs4 import BeautifulSoup

from selenium_driver import start_chrome_driver


def get_detail_urls_from_exhibitor_list(exhibitor_list_url):
    time.sleep(5) # Allow 5 seconds for start Selenium.
    print("Launching Selenium Chrome driver")
    chrome_driver = start_chrome_driver()
    time.sleep(5)  # Allow 5 seconds for setup Chrome driver.
    print("Getting to exhibitor list page")
    chrome_driver.get(
        "https://connections.arabhealthonline.com/widget/event/arab-health-2023-2/exhibitors/RXZlbnRWaWV3XzQyMTQ2Nw=="
    )
    time.sleep(5)  # Allow 5 seconds for the web page to open.

    exhibitors_detail_urls = []
    screen_height = chrome_driver.execute_script("return window.screen.height;")
    i = 1

    # This loop is used for loading the whole page where content 
    # is dynamically loaded while scrolling down.
    print("Loading whole list page")
    while True:
        # scroll one screen height each time
        chrome_driver.execute_script(f"window.scrollTo(0, {screen_height}*{i});")
        i += 1
        time.sleep(1)
        # update scroll height each time after scrolled, as the scroll 
        # height can change after we scrolled the page
        scroll_height = chrome_driver.execute_script("return document.body.scrollHeight;")

        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if screen_height * i > scroll_height:
            break

    print("Saving exhibitors detail urls")
    soup = BeautifulSoup(chrome_driver.page_source, "html.parser")
    for a in soup.select_one(".infinite-scroll-component").find_all("a"):
        exhibitors_detail_urls.append(a.attrs["href"])

    print(f"Number of saved exhibitors detail urls: {len(exhibitors_detail_urls)}")

    # Quitting is extremely important for properly running the next driver.
    chrome_driver.quit()