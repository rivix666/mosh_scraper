"""
    Web Scraper that can be used to download videos from Mosh tutorials site

    Arguments:
    Required arg0: "course_url" eg.:https://codewithmosh.com/courses/enrolled/417695.

    Required arg1: "used_browser" from which we will copy the cookies with login info.
    For now you can use "-f" as firefox or "-c" as chrome.

"""

import sys
import mosh_scrap

if __name__ != "__main__":
    raise AssertionError("This module should be run standalone")

if len(sys.argv) < 3:
    raise AssertionError("You need to pass arguments: -course_url -used_browser")

scraper = mosh_scrap.MoshScraper(sys.argv[1], sys.argv[2])
scraper.download()