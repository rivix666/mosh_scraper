"""TODO"""

import sys


class ProgressBar:
    """TODO"""
    def __init__(self, total_length):
        self.total_length = total_length
        self.__progress = 0

    @property
    def progress(self):
        return self.__progress

    @progress.setter
    def progress(self, value):
        self.__progress = value
        done = int(50 * self.__progress / self.total_length)
        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
        sys.stdout.flush()
