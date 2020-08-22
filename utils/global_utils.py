from enum import Enum


class EBrowser(Enum):
    """ Enum used to identify browser arguments"""
    Firefox = "-f"
    Chrome = "-c"


class GlobalUtils:
    base_url = "https://codewithmosh.com"
    download_dir = "download/"
