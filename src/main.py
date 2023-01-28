from scraper_detail_exhibitor import parse_exhibitor_detail_url
from scraper_list_urls_exhibitors import get_detail_urls_from_exhibitor_list


def run_parsing():
    # get_detail_urls_from_exhibitor_list(None)
    parse_exhibitor_detail_url()

    print("Completed")


if __name__ == "__main__":
    run_parsing()
