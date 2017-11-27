"""
Download audio files.
"""

from os import path, makedirs
import logging
import requests
from . import storage_path


logger = logging.getLogger('orf_archive.oe1_download.download')


def get_filepath(filename):
    dirpath = path.abspath(path.join(storage_path, 'oe1'))
    subdir = filename[:10]
    subdirpath = path.join(dirpath, subdir)
    if not path.exists(subdirpath):
        makedirs(subdirpath)
    return path.join(subdirpath, filename)


def download_file(filename):
    """
    We store the file with its original download name.
    """
    filepath = get_filepath(filename)
    if path.exists(filepath):
        return
    url = 'http://loopstream01.apa.at/?channel=oe1&shoutcast=0&player=oe1_v1&referer=radiothek&userid=8c9f0cdd-c3b3-457c-a261-cf8f153dac0e&id={}&offset=0'.format(filename)
    logger.info('Downloading from {} to {}'.format(url, filepath))
    req = requests.get(url, stream=True)
    if req.status_code == 200:
        with open(filepath, 'wb') as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
