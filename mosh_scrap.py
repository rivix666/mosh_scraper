"""
    Main Mosh-Scrap module

    If you want to use it, just create MoshScraper object with url to course as first argument
    and EBrowser type as second. Ensure you had 'sign in' in chosen browser in to mosh site.

    After that call download method.

    This script will copy cookies from your browser and download all videos from course as logged user.

"""
import requests
import browser_cookie3
from pathlib import Path
from utils import soup_control as sc
from utils.progress_bar import ProgressBar
from utils.global_utils import EBrowser, GlobalUtils


def ensure_dir_exists(directory):
    pth = Path(directory)
    if not pth.exists():
        pth.mkdir()


def download_file(v_data, directory):
    if not v_data:
        return False

    file_path = directory + v_data["name"]
    if Path(file_path).exists():
        print(f"Already exists: ", end="")
        return True

    r = requests.get(v_data["url"], stream=True)
    indicator = ProgressBar(int(r.headers.get('content-length')))
    with open(file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
                indicator.progress += len(chunk)
    return True


def count_urls(urls_data):
    """ Count number of all urls """
    count = 0
    for data in urls_data:
        count += len(data["urls"])
    return count;


class MoshScraper:
    def __init__(self, course_url, browser_arg):
        """
        Create an instance and call download method to use this class

        :param course_url: Link to course eg.:https://codewithmosh.com/courses/enrolled/417695.
        :param browser_arg: browser from which script will copy the cookies with login info. Use EBrowser enum.
        """
        self.course_url = course_url
        self.session = requests.Session()
        if browser_arg == EBrowser.Firefox.value:
            self.session.cookies = browser_cookie3.firefox()
        elif browser_arg == EBrowser.Chrome.value:
            self.session.cookies = browser_cookie3.chrome()
        else:
            self.session.cookies = None
            raise ValueError("Wrong browser argument")

    def download(self):
        """
        Call it to download all files in course.
        It will download them to separate folders per section in directory "download".
        """
        print("---------------- DOWNLOAD BEGIN ----------------")
        urls = self.__get_items_data()
        if urls:
            self.__download_internal(urls)
        else:
            print("Something goes wrong. Script can not find videos links.")
        print("----------------  DOWNLOAD END  ----------------")

    def __get_items_data(self):
        """ :returns List of section titles and videos urls connected with them """
        response = self.__request_response(self.course_url)
        if response:
            sections = sc.find_sections(response.text)
            return [{"title": sc.find_item_title(sec),
                     "urls": sc.gather_items_urls(sec)} for sec in sections]

    def __get_file_data(self, video_url):
        """ :returns List of file names and download urls related to given video """
        response = self.__request_response(video_url)
        if response:
            return sc.gather_download_data(response.text)

    def __download_internal(self, urls):
        ensure_dir_exists(GlobalUtils.download_dir)
        all_urls_num = count_urls(urls)
        index_sum = 0
        for data in urls:
            self.__download_section(data, index_sum, all_urls_num)
            index_sum += len(data["urls"])

    def __download_section(self, sec_data, last_index, all_urls_num):
        section_directory = GlobalUtils.download_dir + sec_data["title"]
        ensure_dir_exists(section_directory)
        for index, url in enumerate(sec_data["urls"]):
            try:
                f_data = self.__get_file_data(url)
            except TypeError:
                print(f" {last_index + index + 1}/{all_urls_num}: Not a video")
            else:
                for file in f_data:
                    if download_file(file, section_directory + "/"):
                        file_name = file["name"]
                        print(f" {last_index + index + 1}/{all_urls_num}: \"{file_name}\" - Downloaded")
                    else:
                        file_name = file["name"]
                        print(f" {last_index + index + 1}/{all_urls_num}: \"{file_name}\" - Can not download")

    def __request_response(self, url):
        try:
            return self.session.get(url)
        except requests.exceptions.RequestException as e:
            print("Exception:", e)
