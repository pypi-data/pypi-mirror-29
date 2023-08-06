import os, urlparse


def detect_filename(url):
    return os.path.basename(urlparse.urlparse(url).path)