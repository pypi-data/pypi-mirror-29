.. image:: https://travis-ci.org/dakrauth/strutil.svg?branch=master
    :target: https://travis-ci.org/dakrauth/strutil


Strutil
=======

Simple helper functions for using strings and regular expressions (mostly) interchangeably.


Requirements
------------

* Python 3.4+

Module Contents
---------------

``strutil.is_string(obj)``

    Check if ``obj`` is a string

``strutil.is_regex(obj)``

    Check if ``obj`` is a regular expression

``strutil.replace(text, old, new, count=None, strip=False)``
    Replace an ``old`` subset of ``text`` with ``new``.

    ``old`` type may be either a string or regular expression.

    If ``strip``, remove all leading/trailing whitespace.

    If ``count``, replace the specified number of occurence, otherwise replace all.

``strutil.remove(text, what, count=None, strip=False)``

    Like ``replace``, where ``new`` replacement is an empty string.

``strutil.replace_each(text, items, count=None, strip=False)``

    Like ``replace``, where each occurrence in ``items`` is a 2-tuple of 
    ``(old, new)`` pair.

``strutil.remove_each(text, items, count=None, strip=False)``

    Like ``remove``, where each occurrence in ``items`` is ``what`` to remove.

``strutil.contains(text, what)``

    Check if ``what`` occurs in ``text``

``strutil.find_first(data, what)``

    Search for ``what`` in the iterable ``data`` and return the index of the 
    first match. Return ``None`` if no match found.

``strutil.splitter(text, token=None, expected=2, default='', strip=False)``

    Split ``text`` by ``token`` into at least ``expected`` number of results.

    When ``token`` is ``None``, the default for Python ``str.split`` is used, 
    which will split on all whitespace.

    ``token`` may also be a regex.

    If actual number of results is less than ``expected``, pad with ``default``.

    If ``strip``, than do just that to each result.



