"""TODO"""

import requests
from enum import Enum
import browser_cookie3
from pathlib import Path
from bs4 import BeautifulSoup
from utils.progress_bar import ProgressBar


class EBrowser(Enum):
    """TODO"""
    Firefox = "-f"
    Chrome = "-c"


def ensure_download_dir_exists():
    pth = Path("download")
    if not pth.exists():
        pth.mkdir()


def download_video(v_data):
    if not v_data:
        return False
    r = requests.get(v_data["url"], stream=True)
    file_name = v_data["name"]
    indicator = ProgressBar(int(r.headers.get('content-length')))
    with open("download/" + file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
                indicator.progress += len(chunk)
    return True


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
        urls = self.get_items_urls()
        self.download_videos(urls)
        print("---------------- DOWNLOAD END ----------------")

    def get_items_urls(self):
        try:
            response = self.session.get(self.course_url)
        except requests.exceptions.RequestException as e:
            print("Exception:", e)
            return
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".section-item")
        return [self.base_url + it.select_one("a.item")["href"] for it in items]

    def get_video_data(self, video_url):
        try:
            response = self.session.get(video_url)
        except requests.exceptions.RequestException as e:
            print("Exception:", e)
            return
        soup = BeautifulSoup(response.text, "html.parser")
        video_url = soup.select_one("a.download")["href"]
        video_name = soup.select_one("a.download")["data-x-origin-download-name"]
        return {"name": video_name, "url": video_url}

    def download_videos(self, urls):
        ensure_download_dir_exists()
        urls_num = len(urls)
        success = failure = 0
        for index, url in enumerate(urls):
            v_data = self.get_video_data(url)
            if download_video(v_data):
                file_name = v_data["name"]
                success += 1
                print(f" {index + 1}/{urls_num}: \"{file_name}\" - Downloaded")
            else:
                file_name = v_data["name"]
                failure += 1
                print(f" {index + 1}/{urls_num}: \"{file_name}\" - Can not download")

    @property
    def base_url(self):
        return "https://codewithmosh.com"
