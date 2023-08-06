#!/usr/bin/env python
import os

from filery.videos import VideoFile
from filery.files import File
from filery.dirs import Directory
from filery.paths import Path


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
