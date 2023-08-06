# encoding: utf-8
"""
json_file_cache.py

Provides class for file based caching of json
"""
import json
from abc import ABCMeta
from .file_cache import FileCache


class JsonFileCache(FileCache):

    __metaclass__ = ABCMeta  # Marks this as an abstract class

    # Also re-implement key and fetch_from_source
    # Optionally modify OBJECT_PAIRS_HOOK

    OBJECT_PAIRS_HOOK = None

    def encode(self,
               data):
        return json.dumps(data)

    def decode(self,
               encoded):
        return json.loads(encoded,
                          object_pairs_hook=self.OBJECT_PAIRS_HOOK)

    def filename(self,
                 key):
        if key.lower().endswith(u'.json'):
            return key
        return u"{key}.json".format(key=key)
