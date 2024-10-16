from cachetools import TTLCache

# Path: backend/core/data_adapter/cache.py

# init cache
cache = TTLCache(maxsize=100000, ttl=60)


def get_cache():
    return cache


def set_cache(key, value):
    cache[key] = value

def is_cache_exists(key):
    return key in cache


def get_cache_value(key):
    return cache.get(key)


def delete_cache(key):
    cache.pop(key, None)


def clear_cache():
    cache.clear()


def get_cache_memory_size():
    return len(cache.keys())
