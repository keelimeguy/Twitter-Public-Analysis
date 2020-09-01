import multiprocessing
import os
import time
from pySmartDL import SmartDL
import math

class DownloaderTools:
    @classmethod
    def download_pysmartdl(cls, link: str):
        """
        Downloads file from link using PySmartDL
        :param link: link that needs to be downloaded
        :return: None
        """
        obj = SmartDL(link, '~/Downloads/', progress_bar=False)
        obj.start(blocking=False)
        while not obj.isFinished():
            print(f"{link} [{obj.get_status()}] {math.floor(obj.get_dl_size() / math.pow(2, 20))} Mb / {math.floor(obj.get_final_filesize() / math.pow(2,20))} Mb @ {obj.get_speed(human=True)} {obj.get_progress_bar()} [{math.floor(100 * obj.get_progress())}%, {obj.get_eta(human=True)} left]")
            time.sleep(1)

    @classmethod
    def download_axel(cls, link: str):
        """
        Downloads file from link using axel
        :param link: link that needs to be downloaded
        :return: None
        """
        os.system(f"axel --verbose --alternate --num-connections={DownloaderTools._connections_count} {link}")

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
