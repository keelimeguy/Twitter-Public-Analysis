import tarfile
import time
from datetime import timedelta
import os


class Preprocess:
    def __init__(self, file: str):
        os.chdir('..')
        self.file = f"{os.getcwd()}/Dozent/~/Downloads/{file}"

    def untar(self):
        '''
        Extracts a single tar directory
        :return: None
        '''
        file = tarfile.open(self.file)
        print('Extracting')
        file.extract('./Preprocess/~/Raw/')


if __name__ == "__main__":
    _start_time = time.time()
    _preprocess_object = Preprocess(file='archiveteam-twitter-stream-2018-02.tar')
    _preprocess_object.untar()
    print(f"Download Time: {timedelta(seconds=(time.time() - _start_time))}")
