.. _quickstart:

==========
Quickstart
==========


.. module:: recipe_caching


This page gives a good introduction in how to get started with Recipe_Caching.
This assumes you already have Recipe_Caching installed. If you do not, head
over to :ref:`Installing Recipe_Caching <install>`.

Let's gets started with some simple use cases and examples.


---------------------------
Setting up the Cache_Region
---------------------------


Cache regions are used by recipe_cache to specify where and how to key the
query cache. Cache region are a concept define in `dogpile.cache`_, and you
can learn more about them there. It needs to be setup in the recipe libraries
SETTINGS object

.. _`dogpile.cache`: https://dogpilecache.readthedocs.io/en/latest/usage.html#region-configuration

::

    from recipe import SETTINGS
    from recipe_caching.regions import build_region

    SETTINGS.CACHE_REGIONS = {
        'default': build_region(region_type='redis', region_args={
                'host': localhost,
                'port': 6379,
                'db': 0,
                'redis_expiration_time': 60*60*2,   # 2 hours
                'distributed_lock': True,
                'lock_timeout': 120,
                'lock_sleep': 5
            }
        )
    }


This is builds the required default cache region using the build_region
shortcut provided by the recipe_caching lib; however, you can also use
the make_region constructor from dogpile.cache.

Next, we need to setup initialize our caching oven.

-----------------------------
Initializing the Caching Oven
-----------------------------
A Caching Oven prepares the SQLAlchemy engine and session for use with
a caching query. This is done by importing the ``get_oven()`` method,
and setting the name to ``'caching'``, which activates the caching oven.

::

    from recipe.oven import get_oven

    oven = get_oven('sqlite://', name='caching')

Now we're ready to setup our Recipe.

-------------------------------
Setting up a Recipe for Caching
-------------------------------

Now that we have a region and an oven, we're now ready to use them to instruct
the recipe to cache it's results or use the cached results if present. To do
this, we set the Recipe's session to a new session build by the oven's
``Session()`` method and add ``'caching'`` to the list of dyanmic_extensions
passed to the Recipe.

::

    from recipe import Recipe

    recipe = Recipe(session=oven.Session(), dynamic_extensions=['caching'])

Now we continue to use the recipe as we would normally.
