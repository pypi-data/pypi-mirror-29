#!/usr/bin/env python
import os

from filer.processors import PathProcessor
from filer.collection import Collection


def list_dirs(path='.', recursive=True, include_parent_dir=False):
    if recursive:
        directories = [
                PathProcessor().process(os.path.join(root, name))
                for root, dirs, files in os.walk(path)
                for name in dirs
            ]

        directories = Collection(directories)
    else:
        directories = tuple(
            [PathProcessor().process(path)]
            +
            [
                PathProcessor.process(os.path.join(path, f))
                for f in os.listdir(path)
                if os.path.isdir(
                    os.path.join(path, f)
                )
            ]
        )
        directories = Collection(directories)
    if include_parent_dir:
        directories = directories + [PathProcessor().process(path)]

    return directories


def list_files(path='.', recursive=True):
    if recursive:
        files = tuple(
            [
                PathProcessor().process(os.path.join(root, name))
                for root, dirs, files in os.walk(path)
                for name in files
                if not os.path.isdir(os.path.join(root, name))
            ]
        )
        files = Collection(files)
        return files
    else:
        files = tuple(
            [
                PathProcessor().process(os.path.join(path, f))
                for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))
            ]
        )
        files = Collection(files)
        return files

