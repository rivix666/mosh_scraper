"""
    Main Mosh-Scrap module

    If you want to use it, just create MoshScraper object with url to course as first argument
    and EBrowser type as second. Ensure you have sign in in chosen browser to mosh site, and use "download" method.

    This script will copy cookies from the browser you choose and then download all videos from course as logged user.

"""

import requests
from enum import Enum
import browser_cookie3
from pathlib import Path
from bs4 import BeautifulSoup
from utils.progress_bar import ProgressBar


class EBrowser(Enum):
    """ Enum used to identify browser arguments"""
    Firefox = "-f"
    Chrome = "-c"


def ensure_dir_exists(directory):
    pth = Path(directory)
    if not pth.exists():
        pth.mkdir()


def download_video(v_data, directory):
    if not v_data:
        return False
    r = requests.get(v_data["url"], stream=True)
    file_name = v_data["name"]
    indicator = ProgressBar(int(r.headers.get('content-length')))
    with open(directory + file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
                indicator.progress += len(chunk)
    return True


def count_urls(urls_data):
    count = 0
    for data in urls_data:
        count += len(data["urls"])
    return count;


class MoshScraper:
    """TODO"""

    def __init__(self, course_url, browser_arg):
        self.course_url = course_url
        self.session = requests.Session()
        if browser_arg == EBrowser.Firefox.value:
            self.session.cookies = browser_cookie3.firefox()
        else:
            self.session.cookies = browser_cookie3.chrome()

    def download(self):
        """TODO"""
        print("---------------- DOWNLOAD BEGIN ----------------")
        urls = self.get_items_data()
        self.download_videos(urls)
        print("---------------- DOWNLOAD END ----------------")

    def get_items_data(self):
        response = self.request_response(self.course_url)
        if response:
            urls = []
            soup = BeautifulSoup(response.text, "html.parser")
            sections = soup.select(".course-section")
            for sec in sections:
                # Prepare section title
                title = sec.select_one(".section-title")
                # Remove unnecessary data from it
                title.select_one(".section-days-to-drip").decompose()
                # Get URLs
                items = sec.select(".section-item")
                urls.append({"title": title.getText().strip(),
                             "urls": [self.base_url + it.select_one("a.item")["href"] for it in items]})
            return urls;

    def get_video_data(self, video_url):
        response = self.request_response(video_url)
        if response:
            soup = BeautifulSoup(response.text, "html.parser")
            video_url = soup.select_one("a.download")["href"]
            video_name = soup.select_one("a.download")["data-x-origin-download-name"]
            return {"name": video_name, "url": video_url}

    def download_videos(self, urls):
        ensure_dir_exists("download")
        urls_num = count_urls(urls)
        success = failure = prev = 0
        for data in urls:
            section_directory = "download/" + data["title"]
            ensure_dir_exists(section_directory)
            for index, url in enumerate(data["urls"]):
                try:
                    v_data = self.get_video_data(url)
                except TypeError:
                    failure += 1
                    print(f" {prev + index + 1}/{urls_num}: Not a video")
                else:
                    if download_video(v_data, section_directory + "/"):
                        file_name = v_data["name"]
                        success += 1
                        print(f" {prev + index + 1}/{urls_num}: \"{file_name}\" - Downloaded")
                    else:
                        file_name = v_data["name"]
                        failure += 1
                        print(f" {prev + index + 1}/{urls_num}: \"{file_name}\" - Can not download")
            prev += len(data["urls"])

    def request_response(self, url):
        try:
            return self.session.get(url)
        except requests.exceptions.RequestException as e:
            print("Exception:", e)

    @property
    def base_url(self):
        return "https://codewithmosh.com"
