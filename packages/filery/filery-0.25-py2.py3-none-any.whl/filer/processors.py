#!/usr/bin/env python
import os

from filer.videos import VideoFile
from filer.files import File
from filer.dirs import Directory
from filer.paths import Path


class PathProcessor(object):

    @staticmethod
    def process(path):
        if os.path.exists(path):
            if os.path.isfile(path):
                return File(path)
            if os.path.isdir(path):
                return Directory(path)
        else:
            return Path(path)
