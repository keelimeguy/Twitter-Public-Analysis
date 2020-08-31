import multiprocessing
import os

from pySmartDL import SmartDL


class DownloaderTools:
    @classmethod
    def download_pysmartdl(cls, link: str):
        """
        Downloads file from link using PySmartDL
        :param link: link that needs to be downloaded
        :return: None
        """
        obj = SmartDL(link, '~/Downloads/')
        obj.start()

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