BGLogs
======

BBGLogs is a wrapper around the logging module of Python,
which includes a few logging setting that are helpful for us.

How to use
----------

The basic usage of ``bglogs`` should be:

.. code:: python

   import bglogs

   def f():
      bglogs.info('Info msg')


The supported functions are the same as in the logging module:
``debug``, ``info``, ``warning``, ``exception``, ``error``, ``critical
but ``log``.

What **bglogs** gives in advantage, is that for every call of any
of those functions, it tries to get the logger using the
convention:


.. code:: python

   logger = logging.getLogger(__name__)

It does so using the ``inspect`` module.
Thus, it is advised that if you are worried about performance,
you should use the convention or pass the name directly as follow:

.. code:: python

   def f():
      bglogs.info('Info msg', _name=__name__)


.. note::

   ``_name`` with a leading underscore has been chosen as parameter
   to avoid conflicts with other possible keyword arguments.




Configuration
-------------

For a **library** in your main ``__init__.py``:

.. code:: python

   import bglogs
   bglogs.configure_as_library()


For an **application**, in you main thread:

.. code:: python

   def main():
       bglogs.configure(debug=False)

This function will configure the root logger
to collect all ``WARNING`` and more severe log messages to the standard error
and the ``INFO`` and ``DEBUG`` messages to the standard output.
However, the default level is ``WARNING``, so ``INFO`` and
``DEBUG`` messages from the libraries will be silenced unless they are
explicitly configured for that.
The main logger of the application will be configured to pass to the root logger
all messages with an ``INFO`` or ``DEBUG`` level according
to the ``debug`` flag.

In addition, you can extend the default configuration by passing a dictionary
with your settings.

The default configuration includes:

- formatters:

  - **bgfmt**: corresponds to ``%(asctime)s %(name)s %(levelname)s -- %(message)s``
    and a date format ``%Y-%m-%d %H:%M:%S``
  - **full**: corresponds to ``%(asctime)s  %(name)s %(levelname)s: %(message)s``
  - **basic**: corresponds to ``%(levelname)s: %(message)s``

- filters:

  - **info**: filters all messages that are not INFO or DEBUG

- handlers

  - **bgout**: send to standard output messages of level DEBUG and INFO
    using *bgfmt* as formatter
  - **bgerr**: send to standard error messages of WARNING and above
    using *bgfmt* as formatter

E.g. to also configure the logging for another library
(whose logger name is ``package``):

.. code:: python

   conf = {'loggers': {
                'package': {
                    'level': 'INFO'
                }
            }}

   bglogs.configure(debug=False, conf=conf)




License
-------

`LICENSE <LICENSE.txt>`_.
