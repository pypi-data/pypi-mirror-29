#!/usr/bin/env python
import os

from filer.utils import get_path_type, get_size, get_inode, atime, mtime, ctime, get_folder_size, \
    get_mime_from_extension


class Path(object):

    type = 'path'

    def __init__(self, path):
        self.initial_path = str(path)
        self.abspath = os.path.abspath(self.initial_path)

    def get_path_type(self):
        return get_path_type(self.get_abspath())

    def get_abspath(self):
        return self.abspath

    def get_dir_name(self):
        return os.path.dirname(self.abspath)

    def get_name_ext(self):
        return os.path.splitext(self.abspath)[1]

    def get_name_base(self):
        return self.get_name()[:-abs(len(self.get_name_ext()))]

    def get_name(self):
        return self.abspath.split('/')[-1]

    def get_size(self):
        return get_size(self.abspath)

    def get_dir_size(self):

        if self.get_exists():

            if self.get_path_type() == 'directory':
                size = get_folder_size(self.abspath)

            elif self.get_path_type() == 'file':
                size = get_folder_size(self.get_dir_name())

            else:
                raise ValueError("Path exists, but is not a directory or file - WTF!!??")
        else:
            size = None

        return size

    def get_inode(self):
        return get_inode(self.abspath)

    def get_realpath(self):
        if self.get_is_link():
            result = os.path.realpath(self.abspath)
            if result == self.abspath:
                raise Exception("Cyclical link - will loop forever")
            return result
        return self.abspath

    def get_is_link(self):
        return os.path.islink(self.abspath)

    def get_exists(self):
        return os.path.exists(self.abspath)

    def get_stat(self):
        return os.stat(self.abspath)

    def get_atime(self):
        return atime(self.abspath)

    def get_mtime(self):
        return mtime(self.abspath)

    def get_ctime(self):
        return ctime(self.abspath)

    def get_mime(self):
        return get_mime_from_extension(self.get_name_ext())

    def get_dropbox_name(self, seperator=''):
        date = self.get_mtime().date().isoformat()
        time = self.get_mtime().time().isoformat()

        if not seperator:
            return '{} {}{}'.format(date, time, self.get_name_ext().lower())
        else:
            return '{}{}{}{}'.format(date, seperator, time, self.get_name_ext().lower())

    def __str__(self):
        return '<{} at {}>'.format(self.__class__.__name__, self.abspath)

    def __repr__(self):
        return '<{} at {}>'.format(self.__class__.__name__, self.abspath)

    def rename(self, new_name):
        dir_name = self.get_dir_name()
        new_name = os.path.join(dir_name, new_name)
        os.rename(self.get_abspath(), new_name)