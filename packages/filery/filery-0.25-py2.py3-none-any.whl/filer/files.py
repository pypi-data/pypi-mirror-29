#!/usr/bin/env python
import hashlib
import os
import shutil
import magic
import xxhash

from filer.paths import Path
from filer.utils import is_file


class File(Path):

    type = 'file'

    # def get_mime(self):
    #     return tuple(magic.from_file(self.get_abspath(), mime=True).split('/'))

    def get_info(self):
        return magic.from_file(self.get_abspath())

    def create_hard_link(self, link_path):
        os.link(self.get_abspath(), link_path)
        return True

    def create_symbolic_link(self, link_path, relative=False):
        if not relative:
            os.symlink(self.get_abspath(), link_path)
            return True

    def copy_file(self, new_path, hard_link=True, symbolic_link=False, preserve_attributes=True):
        if hard_link:
            try:
                self.create_hard_link(new_path)
                return True
            except OSError:
                pass

        elif symbolic_link:
            self.create_symbolic_link(self.get_abspath(), new_path)
            return True

        elif preserve_attributes:
            try:
                shutil.copy2(self.get_abspath(), new_path)
                return True
            except shutil.Error:
                return False

        else:
            shutil.copy(self.get_abspath(), new_path)
        return True

    def open_file(self, mode='r'):
        mode = mode.replace('b', '')
        return open(self.get_abspath(), mode + 'b')

    def read_file(self):
        return self.open_file().read()

    def get_xxhash32(self):
        hash = xxhash.xxh32()
        with open(self.get_abspath(), 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                hash.update(data)
        return hash.hexdigest()

    def get_xxhash64(self):
        hash = xxhash.xxh64()
        with open(self.get_abspath(), 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                hash.update(data)
        return hash.hexdigest()

    def get_md5(self):
        hash = hashlib.md5()
        with open(self.get_abspath(), 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                hash.update(data)
        return hash.hexdigest()

    def get_sha1(self):
        hash = hashlib.sha1()
        with open(self.get_abspath(), 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                hash.update(data)
        return hash.hexdigest()

    def get_sha256(self):
        hash = hashlib.sha256()
        with open(self.get_abspath(), 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                hash.update(data)
        return hash.hexdigest()

    def get_sha512(self):
        hash = hashlib.sha512()
        with open(self.get_abspath(), 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                hash.update(data)
        return hash.hexdigest()

    def get_big_name(self, seperator='_'):
        date = self.get_mtime().date().isoformat()
        time = self.get_mtime().time().isoformat()
        dn = '{}{}{}'.format(date, seperator, time)

        hash = self.get_sha1()
        return '{}{}{}{}'.format(dn, seperator, hash, self.get_name_ext().lower())

    @staticmethod
    def is_file(path):
        return is_file(path)
