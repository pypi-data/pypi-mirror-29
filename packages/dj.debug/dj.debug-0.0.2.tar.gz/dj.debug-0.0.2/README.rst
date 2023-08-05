dj.debug
========

Simple debug utils for Django apps to aid with test-driven development.


|build| |coverage|


Install
-------

.. code-block:: console

  $ pip install dj.debug


For development install

.. code-block:: console

  $ pip install -e git+git@github.com:translate/dj.debug#egg=dj.debug
  $ pip install dj.debug[test]


Initializing the builtin object
-------------------------------

The utils can be imported directly, but the better way is to use `_trace` builtin
functionality.

To activate this call the following, anywhere in your code - eg. in your test settings


.. code-block:: python

   >>> from dj.debug import trace_debug

   >>> trace_debug()

Once this is done, you will have a `_trace` object available anywhere in your environment.

.. code-block:: python

   >>> _trace
   <dj.debug.builtin.Trace object at ...>


You can specify the name of the builtin

.. code-block:: python

   >>> trace_debug("_t")
   >>> _t
   <dj.debug.builtin.Trace object at ...>

Using the builtin object has the advantage that it won't be recognized by linters if you
accidentally leave it in your code.


Usage - pdb
-----------

The `_t` object provides quick access to pdb

.. code-block:: python

   >>> _t.pdb.set_trace()
   --Return--
   > <stdin>(1)<module>()->None
   (Pdb)


Usage - trace debugging
-----------------------

If a line of code that you want to debug is hit many times prior to the point at which you
want to debug it you can use the `_t` object's debug flag

.. code-block:: python

   >>> def commonly_hit_code(*args, **kwargs):
   ...     if _t.debug: _t.pdb.set_trace()

   >>> def some_other_code(*args, **kwargs):
   ...     # we only want to debug after this point
   ...     _t.debug = True
   ...     something_which_triggers_commonly_hit_code()


Usage - sql debugging
---------------------

This tools is useful for finding non-performant code in Django. By tracing the sql that is
being run in blocks of code, you can find and fix querysets that trigger too many queries,
are too complex, have overly large results, etc. You can also use the output in Django's
`dbshell` to analyze, improve and add indeces where appropriate.


.. code-block:: python

   >>> with _t.debug_sql():
   ...     trigger_some_orm_action()



.. |build| image:: https://img.shields.io/travis/translate/dj.debug/master.svg?style=flat-square
        :alt: Build Status
        :target: https://travis-ci.org/translate/dj.debug/branches


.. |coverage| image:: https://img.shields.io/codecov/c/github/translate/dj.debug/master.svg?style=flat-square
        :target: https://codecov.io/gh/translate/dj.debug/branch/master
        :alt: Test Coverage
