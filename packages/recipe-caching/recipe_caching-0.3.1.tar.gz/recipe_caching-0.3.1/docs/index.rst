
Recipe_Caching: A caching solution for Recipe
=============================================

Release v\ |version|. (:ref:`Installation <install>`)

.. Contents:
..
.. .. toctree::
..    :maxdepth: 2
..

.. Indices and tables
.. ==================
..
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`


Recipe_Caching is an MIT licensed caching extension for the recipe querying
library, written in Python. It caches SQL query results keyed by the SQL query.
By providing a custom oven and a recipe extension. Using it requires defining
a `dogpile.cache`_ cache region, using the caching oven, and telling the recipe
to use the caching extension.

.. _`dogpile.cache`: https://dogpilecache.readthedocs.io/en/latest/

.. code-block:: python

    >>> IN_MEMORY_CACHE = {}
    >>> SETTINGS.CACHE_REGIONS = {
            'default': build_region(
                region_type='memory',
                region_arguments={'cache_dict': IN_MEMORY_CACHE}
            )
        }

    >>> oven = get_oven('sqlite://', name='caching')
    >>> Recipe(session=oven.Session(), dynamic_extensions=['caching'])
    ...


User's Guide
------------

This guide covers installation, the core concepts to get you started,
available extensions, connecting to databases and caching.

.. toctree::
   :maxdepth: 2

   intro

.. toctree::
   :maxdepth: 2

   install

.. toctree::
   :maxdepth: 3

   tutorial
   regions


API Reference
-------------

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api

Appendix
--------

.. toctree::
   :maxdepth: 2

   authors
   changelog
