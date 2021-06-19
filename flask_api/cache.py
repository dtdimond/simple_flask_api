from datetime import datetime, timedelta


"""
Methods for maintaining the in-memory data in a cache.
For the sake of this assignment/simplicity, cache_data is a global variable,
   though of course an in-mem db or actual db would offer more resiliency.
Adding or accessing the cache_data will automatically purge data
   that is too old to be worth keeping to keep size manageable.
   
Data is stored in the following format, with the list being sorted
    with newest records at the end for efficiently appending. Also
    considered a two-column pandas df, but appending is somewhat expensive.
cache data format:
    dict[key] -> list[tuple[timestamp, val]]
"""
cache_data = dict()


def reset_cache() -> None:
    """
    Empty the global cache data
    :return: None
    """
    global cache_data
    cache_data = dict()


def get_cache() -> dict:
    """
    Accessor for the global cache data variable
    :return: dict of cache_data
    """
    return cache_data


def get_from_cache(
    key: str,
    delete_older_than: timedelta = timedelta(hours=1),
) -> list[tuple[datetime, int]]:
    """
    Access info in the cache by key, deleting any records older than param
    :param key: key into cache
    :param delete_older_than: amount of time to delete if older than this
    :return: key_data in cache more recent than delete_older_than
    """
    key_data = get_cache().get(key, [])
    delete_old_records(key_data, delete_older_than)
    return key_data


def cache_item(
    key: str,
    item: float,
    delete_older_than: timedelta = timedelta(hours=1),
) -> None:
    """
    Add an item to the cache for a given key, deleting records older than param
    :param key: key into cache
    :param item: value to add to the cache
    :param delete_older_than: amount of time to delete if older than this
    :return: None
    """
    key_data = get_cache().get(key, [])
    delete_old_records(key_data, delete_older_than)
    key_data.append((get_now(), item))
    get_cache()[key] = key_data


def delete_old_records(
    key_data: list[tuple[datetime, int]],
    delete_older_than: timedelta = timedelta(hours=1),
) -> None:
    """
    Delete all key_data records older than delete_older_than
    :param key_data: sorted (oldest first) list of tuple[time, val]
    :param delete_older_than: amount of time to delete if older than this
    :return: None
    """
    now = get_now()
    if (not key_data) or (now - key_data[0][0] <= delete_older_than):
        # Either no data, or oldest record is fresh enough
        return

    # iterate over the list backwards,
    # once a record is detected as too old, delete all above
    i = 0
    for i, (ts, _) in reversed(list(enumerate(key_data))):
        if (now - ts) > delete_older_than:
            break

    key_data[:] = key_data[i+1:]


# To make testing easier
def get_now() -> datetime:
    """
    Purely to make mocking in tests easier
    :return: current time as a datetime
    """
    return datetime.now()



