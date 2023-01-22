import time
import xlsxwriter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

workbook = xlsxwriter.Workbook('database.xlsx')
worksheet = workbook.add_worksheet()

# ----------------------------------------------------------------------------------------------------------------------------
# Fields
# ----------------------------------------------------------------------------------------------------------------------------
F_EXHIBITOR_NAME = "Exhibitor Name"
F_EXHIBITOR_ARAB_HEALTH_ONLINE_PAGE = "Exhibitor Arab Health Online Page"
# Basic fields with same names as on the web:
F_FEATURED_EXHIBITOR = "Featured Exhibitor"
F_COUNTRY_PAVILION = "Country Pavilion"
F_COUNTRY = "Country"
F_COUNTRY_COVERAGE = "Country Coverage"
F_NATURE_OF_BUSINESS = "Nature of Business"
F_INTERESTED_TO_CONNECT_WITH = "Interested to connect with"
F_PRODUCT_CATEGORY_OFFERED = "Product Category Offered"
F_PRODUCT_SUBCATEGORY_OFFERED = "Product Sub-category Offered"
# Social media fields:
F_FACEBOOK = "Facebook"
F_INSTAGRAM = "Instagram"
F_TWITTER = "Twitter"
F_LINKEDIN = "Linkedin"
F_YOUTUBE = "Youtube"
F_PINTEREST = "Pinterest"
# Contact fields:
F_TEL_1 = "Tel 1"
F_TEL_2 = "Tel 2"
F_EMAIL = "Email"
F_WEB_PAGE = "Web Page"
F_ADDRESS = "Address"

# ----------------------------------------------------------------------------------------------------------------------------
# SVG beginning values for recognizing contact fields in html code.
# ----------------------------------------------------------------------------------------------------------------------------
SVG_BEGINNING_VALUES = {
    F_TEL_1: "M33.538",
    F_TEL_2: "M8.664",
    F_EMAIL: "M42.495",
    F_WEB_PAGE: "M23.666",
    F_ADDRESS: "M24.3",
}

# Sets the column number for the fields.
WORKSHEET_FIELDS_COLUMNS = {
    F_EXHIBITOR_NAME: 0,
    F_EXHIBITOR_ARAB_HEALTH_ONLINE_PAGE: 1,
    F_FEATURED_EXHIBITOR: 2,
    F_COUNTRY_PAVILION: 3,
    F_COUNTRY: 4,
    F_COUNTRY_COVERAGE: 5,
    F_NATURE_OF_BUSINESS: 6,
    F_INTERESTED_TO_CONNECT_WITH: 7,
    F_PRODUCT_CATEGORY_OFFERED: 8,
    F_PRODUCT_SUBCATEGORY_OFFERED: 9,
    F_TEL_1: 10,
    F_TEL_2: 11,
    F_EMAIL: 12,
    F_WEB_PAGE: 13,
    F_ADDRESS: 14,
    F_FACEBOOK: 15,
    F_INSTAGRAM: 16,
    F_TWITTER: 17,
    F_LINKEDIN: 18,
    F_YOUTUBE: 19,
    F_PINTEREST: 20,

}

# Write headers into worksheet
for k, v in WORKSHEET_FIELDS_COLUMNS.items():
    worksheet.write(0, v, k)

# Starting row. Rows are zero indexed. Headers are in row: 0
row = 1

with open("my_projects/web_scraper_denca/list_urls_exhibitor_detail.txt", "r") as file:
    for url in file:
        successfully_extracted_detail_page = False

        while not successfully_extracted_detail_page:
            try:
                print(f"Extracted pages: {row}")
                driver.get(url)
                time.sleep(1)  # Allow 1 seconds for the web page to open

                soup = BeautifulSoup(driver.page_source, "html.parser")
                div_all_fields = soup.select_one(".sc-eQGPmX")
                div_basic_fields = div_all_fields.find_all("div", {"class": "sc-kbGplQ"})
                div_social_media_fields = div_all_fields.find_all("a")
                div_contact_fields = div_all_fields.find_all("div", {"class": "sc-gGBfsJ"})

                # Save Exhibitor name.
                exhibitor_name = div_all_fields.select_one(".sc-hMjcWo").text
                worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_EXHIBITOR_NAME], exhibitor_name)

                # Save Exhibitor detail page url from Arab health online web.
                worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_EXHIBITOR_ARAB_HEALTH_ONLINE_PAGE], url)

                # Save Exhibitor basic information
                for field in div_basic_fields:
                    field_name = field.select_one(".sc-exdmVY").text

                    # Fields with one value
                    if field_name in [F_COUNTRY_PAVILION, F_NATURE_OF_BUSINESS, F_FEATURED_EXHIBITOR]:
                        worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[field_name], field.contents[1].text)

                    # Fields with more values
                    elif field_name in [F_COUNTRY, F_COUNTRY_COVERAGE, F_INTERESTED_TO_CONNECT_WITH, F_PRODUCT_CATEGORY_OFFERED,
                                        F_PRODUCT_SUBCATEGORY_OFFERED]:
                        spans = field.find_all("span", {"class": "sc-fATqzn"})
                        worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[field_name], ", ".join([s.text for s in spans]))

                # Save Exhibitor contact information
                for field in div_contact_fields:
                    # Exclude contact field in header on exhibitor detail page
                    if "sc-hMjcWo" not in field.previous_sibling.attrs["class"]:

                        svg_path = field.select_one("path").attrs["d"]
                        text = field.select_one("a").text

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

                # Save Exhibitor social media information
                for field in div_social_media_fields:
                    href = field["href"]

                    if F_FACEBOOK.lower() in href:
                        worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_FACEBOOK], href)
                    elif F_INSTAGRAM.lower() in href:
                        worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_INSTAGRAM], href)
                    elif F_TWITTER.lower() in href:
                        worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_TWITTER], href)
                    elif F_LINKEDIN.lower() in href:
                        worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_LINKEDIN], href)
                    elif F_PINTEREST.lower() in href:
                        worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_PINTEREST], href)
                    elif F_YOUTUBE.lower() in href:
                        worksheet.write(row, WORKSHEET_FIELDS_COLUMNS[F_YOUTUBE], href)

                successfully_extracted_detail_page = True

            except Exception as exception:
                print(exception)

        row += 1

workbook.close()
driver.close()


def parse_exhibitor_detail_url(exhibitor_detail_url):
    pass