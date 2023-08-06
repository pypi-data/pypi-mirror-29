.. _api:

===
API
===



This part of the documentation covers all the interfaces of Recipe_Caching.


-------------------
Caching Oven Object
-------------------


.. module:: recipe_caching.oven.drivers.caching_oven
.. autoclass:: CachingOven
   :inherited-members:


-----------------------
CachingQueryHook Object
-----------------------


.. module:: recipe_caching.hooks.modify_query
.. autoclass:: CachingQueryHook
   :inherited-members:

Supporting Objects

------------------------------------
CachingQuery Object (Query subclass)
------------------------------------


.. module:: recipe_caching.caching_query
.. autoclass:: CachingQuery

-------
Mappers
-------



.. module:: recipe_caching.mappers
.. autoclass:: FromCache
   :inherited-members:

.. autoclass:: RelationshipCache
   :inherited-members:

-------
Regions
-------

.. module:: recipe_caching.regions
.. autofunction:: build_region

.. autofunction:: mangle_key

.. autofunction:: unicode_sha1_mangle_key

.. autofunction:: async_creation_runner

.. autofunction:: clean_unicode
