import unittest

from Dozent.downloader_tools import DownloaderTools

from pySmartDL import SmartDL
from pySmartDL.control_thread import ControlThread
from collections import namedtuple
import threading

DownloadProgress = namedtuple('DownloadProgress', 'dl_size filesize speed')


class DownloaderToolsTestCase(unittest.TestCase):
    def test_make_progress_status(self):

        url = 'https://www.google.com/'

        # We want to initialize the SmartDL object without actually starting the download
        downloader_obj = SmartDL(url)
        downloader_obj.post_threadpool_thread = threading.Thread(target=lambda: None)

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
            progress_percentage = 100.0 * progress.dl_size / progress.filesize if progress.filesize else 0

            expected_prefix = f"[finished] {progress.dl_size}Mb/{progress.filesize}Mb " \
                f"@{progress.speed} {'B' if progress.speed else 'bytes'}/s"

            expected_suffix = f"[{int(progress_percentage):3.0f}%, {0:3.0f}sec left]"

            actual_progress_percentage, actual_prefix, actual_suffix = DownloaderTools._make_progress_status(downloader_obj)

            self.assertAlmostEqual(progress_percentage, actual_progress_percentage)
            self.assertEqual(expected_prefix, actual_prefix)
            self.assertEqual(expected_suffix, actual_suffix)


if __name__ == "__main__":
    unittest.main()
