cachinhgutil
============
A hierarchy of classes to provide caching functionality
with minimal fuss.

When using the cache, just use the fetch method.
This will pull from the cache if it's present and
not expired otherwise will use 'fetch_from_source'.

Cache
-----
Abstract class.
Not expected to be used. Provides the methods
needed by subclasses provided by the package.

Methods that need to be implemented in the concrete class:
    key
    fetch_from_source
    cache
    fetch_from_cache_by_key
    delete_by_key
    expiry_time

Optional:
    cook

BaseMemoryClass
---------------
Abstract class.

Methods that must be implemented in concrete class:
    key
    fetch_from_source
    calculate_expiry
Optional:
    cook

SimpleMemoryClass
-----------------
Abstract class.

Methods that must be implemented in concrete class:
    key
    fetch_from_source
Optinal:
    cook

BaseHttpMemoryCache
-------------------
Abstract class.

Caches requests objects or objects generated from requests.

TODO: Improve expiry calculations. Currently only uses max age.

Methods that must be implemented in concrete class:
    key
    fetch_from_source
    get_request_for_item (if caching objects generated from request objects)
Optinal:
    cook

HttpMemoryCache
---------------
Concrete class.

Uses the url string as the key.
Uses requests.get as fetch_from_source.

Use:
Instantiate and use instance.fetch(url) to fetch from the cache or source.

BinaryFileCache
---------------
Abstract class.

Reads from and writes to binary files. Suitable for caching
images.

Methods that must be implemented in concrete class:
    key
    fetch_from_source
Optional:
    cook

FileCache
---------
Abstract class.

Reads from and writes to files with encoding.

Methods that must be implemented in concrete class:
    key
    fetch_from_source
Optional:
    cook
    encode
    decode

JsonFileCache
-------------
Abstract class.

This is just FileCache with JSON encoding and decoding.

fetch_from_source should return a JSON string.
If OBJECT_PAIRS_HOOK is set, then decode will
use that. Typically use: collections.OrderedDict
to retain the order of elements.

Methods that must be implemented in concrete class:
    key
    fetch_from_source

Optional:
    cook
    OBJECT_PAIRS_HOOK

TwoLevelCache
-------------
Concrete class.

Generally this means an in-memory cache joined to a
persistent cache (e.g, file, database). That means
your cache persists over many executions, but doesn't
need to access the slower persistent cache more than
once per item fetched.

To use it, implement the two caches and instantiate
TwoLevelCache to join them. Pass in-memory cache class
as the transient_cache and the persistent cache class
as (surprise!) the pesistent_cache.



