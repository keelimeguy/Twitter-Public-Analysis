import unittest

from Dozent.DownloaderTools import DownloaderTools

from pySmartDL import SmartDL
from pySmartDL.control_thread import ControlThread
from collections import namedtuple

DownloadProgress = namedtuple('DownloadProgress', 'dl_size filesize speed')


class DownloaderToolsTestCase(unittest.TestCase):
    def test_make_progress_status(self):

        url = 'https://www.google.com/'

        # We want to initialize the SmartDL object without actually starting the download
        downloader_obj = SmartDL(url)
        control_thread = ControlThread(downloader_obj)
        downloader_obj.control_thread = control_thread

        for progress in [
            DownloadProgress(dl_size=0, filesize=0, speed=0),
            DownloadProgress(dl_size=1024, filesize=1048576, speed=42),
            DownloadProgress(dl_size=129864, filesize=129865, speed=777),
            DownloadProgress(dl_size=999999, filesize=999999, speed=999),
        ]:
            assert(progress.speed < 1000)

            # We create faked download progress to test the output
            downloader_obj.shared_var.value = progress.dl_size << 20
            downloader_obj.filesize = progress.filesize << 20
            control_thread.dl_speed = progress.speed
            progress_percentage = int(100 * progress.dl_size / progress.filesize) if progress.filesize else 0

            expected_output = f"\r {url} [ready] {progress.dl_size} Mb / {progress.filesize} Mb " \
                f"@ {progress.speed} {'B' if progress.speed else 'bytes'}/s " \
                f"[{'#' if progress_percentage == 100 else '-'}] [{progress_percentage}%, 0 seconds left]"

            self.assertEqual(expected_output, DownloaderTools._make_progress_status(downloader_obj, 3))


if __name__ == "__main__":
    unittest.main()
