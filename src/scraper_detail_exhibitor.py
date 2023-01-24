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
    F_TEL_1 = "Tel 1"
    F_TEL_2 = "Tel 2"
    F_EMAIL = "Email"
    F_WEB_PAGE = "Web Page"

    # ----------------------------------------------------------------------------------------------------------------------------
    # SVG beginning values for recognizing contact fields in html code.
    # ----------------------------------------------------------------------------------------------------------------------------
    SVG_BEGINNING_VALUES = {
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
        F_TEL_1: 4,
        F_TEL_2: 5,
        F_EMAIL: 6,
        F_WEB_PAGE: 7,
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
                    # print(f"Extracted pages: {row}")
                    chrome_driver.get(url)
                    time.sleep(1)  # Allow 1 seconds for the web page to open
                    soup = BeautifulSoup(chrome_driver.page_source, "html.parser")

                    # Save Exhibitor name.
                    exhibitor_name = soup.select_one(".hQJFGn").text
                    worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_EXHIBITOR_NAME], exhibitor_name)

                    # Save Exhibitor detail page url from Arab health online web.
                    worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_EXHIBITOR_ARAB_HEALTH_ONLINE_PAGE], url)

                    # Save Exhibitor country.
                    div_label_country = soup.find("div", text="Country")
                    if div_label_country:
                        print(div_label_country)
                        div_label_country_next_sibling = div_label_country.next_sibling
                        exhibitor_country = div_label_country_next_sibling.find("span").text
                        worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_COUNTRY], exhibitor_country)


                    # # Save Exhibitor basic information
                    # for field in div_basic_fields:
                    #     field_name = field.select_one(".sc-exdmVY").text

                    #     # Fields with one value
                    #     if field_name in [F_COUNTRY_PAVILION, F_NATURE_OF_BUSINESS, F_FEATURED_EXHIBITOR]:
                    #         worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[field_name], field.contents[1].text)

                    #     # Fields with more values
                    #     elif field_name in [F_COUNTRY, F_COUNTRY_COVERAGE, F_INTERESTED_TO_CONNECT_WITH, F_PRODUCT_CATEGORY_OFFERED,
                    #                         F_PRODUCT_SUBCATEGORY_OFFERED]:
                    #         spans = field.find_all("span", {"class": "sc-fATqzn"})
                    #         worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[field_name], ", ".join([s.text for s in spans]))

                    # Save Exhibitor contact information
                    # for field in div_contact_fields:
                    #     # Exclude contact field in header on exhibitor detail page
                    #     if "sc-hMjcWo" not in field.previous_sibling.attrs["class"]:
                    #
                    #         svg_path = field.select_one("path").attrs["d"]
                    #         text = field.select_one("a").text
                    #
                    #         if svg_pat  h.startswith(SVG_BEGINNING_VALUES[F_TEL_1]):
                    #             worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_TEL_1], text)
                    #         elif svg_path.startswith(SVG_BEGINNING_VALUES[F_TEL_2]):
                    #             worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_TEL_2], text)
                    #         elif svg_path.startswith(SVG_BEGINNING_VALUES[F_EMAIL]):
                    #             worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_EMAIL], text)
                    #         elif svg_path.startswith(SVG_BEGINNING_VALUES[F_WEB_PAGE]):
                    #             worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_WEB_PAGE], text)
                    #         elif svg_path.startswith(SVG_BEGINNING_VALUES[F_ADDRESS]):
                    #             worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_ADDRESS], text)

                    successfully_extracted_detail_page = True

                except Exception as exception:
                    print(exception)
                    print(url)
                    print(soup.select_one(".hQJFGn"))
                    print(div_label_country_next_sibling.find("span"))

            row += 1
            print(f"Number of saved Exhibitors: {row}")

    workbook.close()
    chrome_driver.close()
