.. _intro:

Introduction
============

Recipe_Caching is an extension to `recipe`_ the cross-database querying
library. It allows you to cache SQL statements and their results in a wide
array of caching backends. It uses `dogpile.cache`_ to store and manage
the cache.

.. _`recipe`: http://github.com/juiceinc/recipe/
.. _`dogpile.cache`: https://dogpilecache.readthedocs.io/en/latest/

Recipe_Caching License
----------------------

Recipe_Caching is released under terms of `The MIT License`_.

::

    Copyright 2017 Chris Gemignani

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

.. _`The MIT License`: http://www.opensource.org/licenses/mit-license.php



.. _pythonsupport:

Pythons Supported
-----------------

At this time, the following Python platforms are officially supported:

* cPython 2.7
* cPython 3.6

Support for other Pythons will be rolled out soon.


Now, go :ref:`Installing Recipe_Caching <install>`.
