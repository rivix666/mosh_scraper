from bs4 import BeautifulSoup


def find_sections(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.select(".course-section")


def find_item_title(section):
    # Prepare section title
    title = section.select_one(".section-title")
    # Remove unnecessary data from it
    title.select_one(".section-days-to-drip").decompose()
    return title.getText().strip()


def gather_items_urls(section):
    items = section.select(".section-item")
    return ["https://codewithmosh.com" + it.select_one("a.item")["href"] for it in items]


def gather_download_data(html):
    soup = BeautifulSoup(html, "html.parser")
    download_items = soup.select("a.download")
    return [{"name": dl["data-x-origin-download-name"],
             "url": dl["href"]} for dl in download_items]
