import time
import xlsxwriter
from bs4 import BeautifulSoup
from selenium_client import start_chrome_driver


def parse_exhibitor_detail_url():
    time.sleep(10)  # Allow 10 seconds for start Selenium.
    print("Launching Selenium Chrome driver")
    chrome_driver = start_chrome_driver()

    workbook = xlsxwriter.Workbook('database.xlsx')
    worksheet = workbook.add_worksheet()

    # ----------------------------------------------------------------------------------------------------------------------------
    # Fields
    # ----------------------------------------------------------------------------------------------------------------------------
    F_EXHIBITOR_NAME = "Exhibitor Name"
    F_EXHIBITOR_ARAB_HEALTH_ONLINE_PAGE = "Exhibitor Arab Health Online Page"
    F_FEATURED_EXHIBITOR = "Featured Exhibitor"
    F_COUNTRY = "Country"
    F_ADDRESS = "Address"
    F_TEL_1 = "Tel 1"
    F_TEL_2 = "Tel 2"
    F_EMAIL = "Email"
    F_WEB_PAGE = "Web Page"

    # ----------------------------------------------------------------------------------------------------------------------------
    # SVG beginning values for recognizing contact fields in html code.
    # ----------------------------------------------------------------------------------------------------------------------------
    SVG_BEGINNING_VALUES = {
        F_ADDRESS: "M15 10a3",
        F_TEL_1: "M15 6a1",
        F_TEL_2: "M19 15a1",
        F_EMAIL: "M12.924",
        F_WEB_PAGE: "M10.342",
    }

    # Sets the column number for the fields.
    WORKSHEET_FIELDS_COLUMNS = {
        F_EXHIBITOR_NAME: 0,
        F_EXHIBITOR_ARAB_HEALTH_ONLINE_PAGE: 1,
        F_FEATURED_EXHIBITOR: 2,
        F_COUNTRY: 3,
        F_ADDRESS: 4,
        F_TEL_1: 5,
        F_TEL_2: 6,
        F_EMAIL: 7,
        F_WEB_PAGE: 8,
    }

    # Write headers into worksheet
    for k, v in WORKSHEET_FIELDS_COLUMNS.items():
        worksheet.write(0, v, k)

    # Starting row. Rows are zero indexed. Headers are in row: 0
    row = 1

    print("Opening file: 'exhibitors_detail_urls.txt'")
    with open("exhibitors_detail_urls.txt", "r") as file:
        for url in file:
            successfully_extracted_detail_page = False

            while not successfully_extracted_detail_page:
                try:
                    chrome_driver.get(url)
                    time.sleep(4)  # Allow 4 seconds for the web page to open. This is minimum now.
                    soup = BeautifulSoup(chrome_driver.page_source, "html.parser")

                    # Save Exhibitor name.
                    exhibitor_name = soup.select_one(".hQJFGn").text
                    worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_EXHIBITOR_NAME], exhibitor_name)

                    # Save Exhibitor detail page url from Arab health online web.
                    worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_EXHIBITOR_ARAB_HEALTH_ONLINE_PAGE], url)

                    # Save featured exhibitor boolean.
                    div_label_featured_exhibitor = soup.find("div", text="Type")
                    if div_label_featured_exhibitor:
                        worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_FEATURED_EXHIBITOR], "yes")
                    else:
                        worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_FEATURED_EXHIBITOR], "no")

                    # Save Exhibitor country.
                    div_label_country = soup.find("div", text="Country")
                    if div_label_country:
                        div_label_country_next_sibling = div_label_country.next_sibling
                        exhibitor_country = div_label_country_next_sibling.find("span").text
                        worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_COUNTRY], exhibitor_country)

                    # Save Exhibitor contact information
                    for element_anchor in soup.select(".jZUzxX"):
                        svg_path = element_anchor.parent.previous_sibling.next.next.attrs["d"]
                        text = element_anchor.next.text

                        if svg_path.startswith(SVG_BEGINNING_VALUES[F_TEL_1]):
                            worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_TEL_1], text)
                        elif svg_path.startswith(SVG_BEGINNING_VALUES[F_TEL_2]):
                            worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_TEL_2], text)
                        elif svg_path.startswith(SVG_BEGINNING_VALUES[F_EMAIL]):
                            worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_EMAIL], text)
                        elif svg_path.startswith(SVG_BEGINNING_VALUES[F_WEB_PAGE]):
                            worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_WEB_PAGE], text)
                        elif svg_path.startswith(SVG_BEGINNING_VALUES[F_ADDRESS]):
                            worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_ADDRESS], text)

                    successfully_extracted_detail_page = True

                except Exception as exception:
                    print(exception)

            row += 1
            print(f"Number of saved Exhibitors: {row}")

            if row == 100:
                break

    workbook.close()
    chrome_driver.close()
