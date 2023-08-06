Introduction
============

.. image:: https://secure.travis-ci.org/pyrenees/plone.synchronize.png
   :target: http://travis-ci.org/pyrenees/plone.synchronize

This package provides a simple decorator to help synchronize methods across
threads, to avoid problems of concurrent access.

It can be used like this::

    from threading import Lock
    from plone.synchronize import synchronized

    class StupidStack(object):

        _elements = [] # not thread safe
        _lock = Lock()

        @synchronized(_lock)
        def push(self, item):
            self._elements.append(item)

        @synchronized(_lock)
        def pop(self):
            last = self._elements[-1]
            del self._elements[-1]
            return last

The decorator takes care of calling lock.acquire() just before the method
is executed, and lock.release() just after. If an exception is raised in the
method, the lock will still be released.

Changelog
=========

1.0.3 (2018-03-10)
------------------

Bug fixes:

- Release it as a wheel as well as an egg.
  [gforcada]

1.0.2 (2016-11-01)
------------------

New features:

- Test Python 3 compatibility.
  [datakurre]


1.0.1 - 2011-05-20
------------------

* Add license metadata.
  [davisagli]

1.0 - 2011-04-30
----------------

* No changes

1.0b1 - 2009-03-30
------------------

* Initial release


