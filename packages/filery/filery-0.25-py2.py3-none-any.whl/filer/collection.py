#!/usr/bin/env python

from __future__ import absolute_import, print_function
from os.path import isfile, isdir


class Collection(list):

    def get_items(self):
        return self

    def tolist(self):
        return list(self)

    def get_num_items(self):
        return len(self)

    def get_files(self, tolist=False):
        if not tolist:
            return Collection([item for item in self.get_items() if isfile(item.get_abspath())])
        else:
            return [item for item in self.get_items() if isfile(item.get_abspath())]

    def get_dirs(self, tolist=False):
        if not tolist:
            return Collection([item for item in self.get_items() if isdir(item.get_abspath())])
        else:
            return [item for item in self.get_items() if isdir(item.get_abspath())]

    def get_images(self, tolist=False):
        if not tolist:
            return Collection([item for item in self.get_files().get_items() if item.get_mime()[0] == 'image'])
        else:
            return [item for item in self.get_files().get_items() if item.get_mime()[0] == 'image']

    def get_pngs(self, tolist=False):
        if not tolist:
            return Collection([item for item in self.get_images().get_items() if item.get_mime()[1] == 'png'])
        else:
            return [item for item in self.get_images().get_items() if item.get_mime()[1] == 'png']

    def get_jpgs(self, tolist=False):
        if not tolist:
            return Collection([item for item in self.get_images().get_items() if item.get_mime()[1] == 'jpg' or item.get_mime()[1] == 'jpeg'])
        else:
            return [item for item in self.get_images().get_items() if item.get_mime()[1] == 'jpg' or item.get_mime()[1] == 'jpeg']

    def get_gifs(self, tolist=False):
        if not tolist:
            return Collection([item for item in self.get_files().get_items() if item.get_mime()[0] == 'gif'])
        else:
            return [item for item in self.get_files().get_items() if item.get_mime()[0] == 'gif']

    def get_tiffs(self, tolist=False):
        if not tolist:
            return Collection([item for item in self.get_files().get_items() if item.get_mime()[0] == 'tiff'])
        else:
            return [item for item in self.get_files().get_items() if item.get_mime()[0] == 'tiff']

    def copy_files(self, file_path_string):
        for item in self.get_files().get_items():
            item.copy_file(file_path_string, hard_link=False, symbolic_link=False, preserve_attributes=True)


