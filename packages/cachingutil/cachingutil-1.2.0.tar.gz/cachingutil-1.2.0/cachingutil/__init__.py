# -*- coding: utf-8 -*-
"""
cachingutil

Copyright (c) 2017 Hywel Thomas. All rights reserved.
"""

# Get module version
from ._metadata import __version__

# Import key items from module
from .base_cache import CacheError
from .memory_cache import (BaseMemoryCache,
                           BaseHttpMemoryCache,
                           SimpleMemoryCache,
                           HttpMemoryCache)
from .binary_file_cache import BinaryFileCache
from .file_cache import FileCache
from .json_file_cache import JsonFileCache
from .double_cache import TwoLevelCache

# Set default logging handler to avoid "No handler found" warnings.
from logging import NullHandler, getLogger
getLogger(__name__).addHandler(NullHandler())
