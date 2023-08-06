#!/usr/bin/env python
import os

from filer.paths import Path
from filer.utils import is_dir


class Directory(Path):
    type = 'directory'

    @staticmethod
    def is_dir(path):
        return is_dir(path)
