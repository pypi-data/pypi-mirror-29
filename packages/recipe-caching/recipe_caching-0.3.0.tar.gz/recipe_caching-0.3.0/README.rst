========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1


.. |downloads| image:: https://img.shields.io/pypi/dm/recipe.svg
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/recipe

.. |wheel| image:: https://img.shields.io/pypi/wheel/recipe.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/recipe

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/recipe.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/recipe

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/recipe.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/recipe


.. end-badges

Recipe_Caching is an MIT licensed caching extension for the recipe querying
library, written in Python. It caches SQL query results keyed by the SQL query.
By providing a custom oven and a recipe extension. Using it requires defining
a `dogpile.cache`_ cache region, using the caching oven, and telling the recipe
to use the caching extension.

Installation
============

::

    pip install recipe_caching

Documentation
=============

https://recipe_caching.readthedocs.io/

Development
===========

To run the all tests run::

    py.test
