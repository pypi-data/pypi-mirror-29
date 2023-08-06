#!/usr/bin/env python
import os

import magic


def is_video(path):
    abspath = os.path.abspath(path)
    type = tuple(magic.from_file(abspath, mime=True).split('/'))[0]
    if type == 'video':
        return True
    else:
        return False