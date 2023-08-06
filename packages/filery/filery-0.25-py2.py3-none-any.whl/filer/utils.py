#!/usr/bin/env python
import datetime
import os
import string
from os.path import exists
from os.path import isdir
from os.path import isfile

try:
    from str import maketrans
except ImportError:
    from string import maketrans

import magic

from filer.info import MIME_EXTENSION_DICT


# For backwards compatibility. Previously, this module include unnecessary functions:
# def is_dir() and def is_file().
from os.path import isdir as is_dir
from os.path import isfile as is_file


def remove_nondigits(string_arg):
    """
    Removes all non-digits (letters, symbols, punctuation, etc.)
    :param str:
    :return: string consisting only of digits
    :rtype: str
    """
    all = maketrans('', '')
    nodigs = all.translate(all, string.digits + '.')
    return string_arg.translate(all, nodigs)


def get_path_type(path):
    """
    Gets the type of a path. Acceptable return values: 'directory', 'file', and ''.
    :param str path:
    :return: 'directory', 'file', and ''
    :rtype: str
    """

    if exists(path):
        if isfile(path):
            return 'file'
        elif isdir(path):
            return 'directory'
        raise ValueError('Path exists, but is neither file nor directory. WTF!!??')

    return ''


def is_image(path):
    if isfile(path):
        mime = tuple(magic.from_file(path, mime=True).split('/'))
        if mime[0] == 'image':
            return True
    return False


def get_size(path):
    return os.stat(path).st_size


def get_inode(path):
    return os.stat(path).st_ino


def atime(path):
    return datetime.datetime.fromtimestamp(os.stat(path).st_atime)


def mtime(path):
    return datetime.datetime.fromtimestamp(os.stat(path).st_mtime)


def ctime(path):
    return datetime.datetime.fromtimestamp(os.stat(path).st_ctime)


def get_folder_size(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += get_folder_size(itempath)
    return total_size


def get_mime_from_extension(extension):
    if extension[0] == '.':
        extension = extension[1:]
    mime_string = MIME_EXTENSION_DICT.get(str(extension))
    if mime_string:
        mime_list = mime_string.split('/')
        mime_tuple = tuple(mime_list)
        return mime_tuple
    return tuple([None, None])


