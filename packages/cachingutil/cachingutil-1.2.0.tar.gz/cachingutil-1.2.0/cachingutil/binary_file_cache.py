# encoding: utf-8
"""
binary_file_cache.py

Provides class for caching binary data in files.
"""

from abc import ABCMeta
from .base_file_cache import BaseFileCache


class BinaryFileCache(BaseFileCache):

    __metaclass__ = ABCMeta  # Marks this as an abstract class

    # Also re-implement fetch_from_source and key

    def read(self,
             filepath):
        with open(filepath,
                  mode=u'rb') as cached_file:
            return cached_file.read()

    def write(self,
              item,
              filepath):
        with open(filepath,
                  mode=u'wb') as cached_file:
            cached_file.write(item)
