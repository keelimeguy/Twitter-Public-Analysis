import multiprocessing
import os
import time
from pySmartDL import SmartDL
import math


class DownloaderTools:
    @classmethod
    def download_pysmartdl(cls, link: str, verbose=True):
        """
        Downloads file from link using PySmartDL
        :param link: link that needs to be downloaded
        :param verbose: Show verbose output
        :return: None
        """
        downloader_obj = SmartDL(link, '~/Downloads/', progress_bar=False)
        downloader_obj.start(blocking=False)
        while not downloader_obj.isFinished():
            if verbose:
                print(DownloaderTools._make_progress_status(downloader_obj, link))
            time.sleep(1)

    @staticmethod
    def _make_progress_status(downloader_obj: SmartDL, link, progress_bar_length=20) -> str:
        """
        Function to make progress bar
        :param downloader_obj: SmartDL object that's currently downloading a file
        :param link: Link that the SmartDL object is downloading from
        :param progress_bar_length: Length of the progress bar
        :return: returns the progress bar as a string format
        """

        status = downloader_obj.get_status()
        num1 = math.floor(downloader_obj.get_dl_size() / math.pow(2, 20))
        num2 = math.floor(downloader_obj.get_final_filesize() / math.pow(2, 20))
        speed = downloader_obj.get_speed(human=True)
        progress_bar = downloader_obj.get_progress_bar(length=progress_bar_length)
        progress_percentage = math.floor(100 * downloader_obj.get_progress())
        eta = downloader_obj.get_eta(human=True)

        return f"{link} [{status}] {num1} Mb / {num2} Mb @ {speed} {progress_bar} " \
               f"[{progress_percentage}%, {eta} left]"

    @classmethod
    def download_axel(cls, link: str):
        """
        Downloads file from link using axel
        :param link: link that needs to be downloaded
        :return: None
        """
        os.system(
            f"axel --verbose --alternate --num-connections={DownloaderTools._connections_count} {link}")

    @classmethod
    def download_aria2(cls, link: str):
        """
        Downloads file from link using aria2
        :param link: link that needs to be downloaded
        :return: None
        """
        os.system(f"aria2c -x {DownloaderTools._connections_count} {link}")

    _connections_count = 2 * multiprocessing.cpu_count()


_downloaders = {
    'pySmartDL': DownloaderTools.download_pysmartdl,
    'Axel': DownloaderTools.download_axel,
    'aria2': DownloaderTools.download_aria2
}

if __name__ == "__main__":
    pass
