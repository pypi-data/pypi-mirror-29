.. _region:

========================
More About Cache Regions
========================

While we took a quick look at creating a redis region in the :ref:`quickstart`,
there is still alot more to cover about regions. Let's start by talking about
our quickstart ``build_region`` function.


------------
build_region
------------

The ``build_region`` function uses a quick set of defaults to get you caching
fast and effeciently. It builds a cache region using the backend type you
supply coupled with the region arguments, and a sha1 based cache key instead of
the full query text. These sha1 are prefixed with a ``recipe_cache:``. You can
also add a ``CACHE_PREFIX`` to the recipe ``SETTINGS`` object to have it
appended to the key prefix.

For the cache backend type, you can use any supported by dogpile.cache:

- memory
- memcached
- pylibmc
- bmemcached
- redis
- dbm
- null

The region arguments vary by backend, but they are a dictionary of
configuration details required to connect to the cache backend. You can get
all the details about options by backend type in the `dogpile.cache documentation`_.

.. _`dogpile.cache documentation`: https://dogpilecache.readthedocs.io/en/latest/api.html#module-dogpile.cache.backends.memory

While you are required to supply the region_type and region_arguments, behind
the scenes we are defining a function that creates the cache entries in
a seperate thread, and a system to make prefixed sha1 based cache keys. In
``dogpile.cache`` terminology, these are the ``async_creation_runner`` and
``key_mangler`` arguments to ``dogpile.cache``'s' ``make_region`` function.

In additional to our ``build_region`` function, you can also use the full
power of ``dogpile.cache``'s ``make_region`` function.'

---------------------------
Dogpile.cache's make_region
---------------------------

The ``make_region`` function can be used to cache regions as well. The
recipe_caching library only supports the ``'default'`` region. You can get
more information about ``make_region`` in the dogpile.cache documentation.

If you decide to make your own cache regions. We highly encourage you to
implement the ``async_creation_runner`` and ``key_mangler`` arguments.
