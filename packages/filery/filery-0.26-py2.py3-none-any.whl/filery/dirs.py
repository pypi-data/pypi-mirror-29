#!/usr/bin/env python
import os

from filery.paths import Path
from filery.utils import is_dir


class Directory(Path):
    type = 'directory'

    @staticmethod
    def is_dir(path):
        return is_dir(path)
