verbosity
=========

python package to easily add verbosity levels and debug options to
command line tools developed in python. Verbosity add the folloing
argparse arguments:

-  -v, –verbosity increase output verbosity: INFO, DEBUG, DEEPDEBUG

   Increase the instances to move from INFO (-v) and DEBUG (-vv) both
   local to logger used when initializing verbosity, typically main(),
   and DEEPDEBUG (-vvv) which will initalize the rootlogger and catch
   any unhandled logging events from any other packages loaded which use
   logging.

-  -vbl VBLACKLIST [VBLACKLIST …], –vblacklist VBLACKLIST [VBLACKLIST …]

   | *Blacklist of modules and functions to ignore when logging*
   | Any functions listed will have their logging ignored. This is great
     to exclude really noisy functions you’re not interested in.

-  -vwl VWHITELIST [VWHITELIST …], –vwhitelist VWHITELIST [VWHITELIST …]

   *Whitelist of modules and functions to include when logging* Only
   functions listed here will have logging output. This is implemented
   internally by setting DEEPDEBUG and then filtering out all messages
   except from functions on the whitelist and matching the level
   specified with -v

logging
~~~~~~~

Currently verbosity acts on either the specified logger or the root
logger for setting the loglevel, and on the root logger’s
*StreamHandler* for filtering.

This library directly supports the use of the *argparse* and *logging*
libraries. To use this library:

1. Per Python’s `Advanced Logging
   Tutorial <https://docs.python.org/3/howto/logging.html>`__ initiate a
   logger in each module which uses logging. For example:

.. code:: python

    import logging
    logger = logging.getLogger(__name__)

2. Using `argparse <https://docs.python.org/3/library/argparse.html>`__,
   setup your parser and add any relevant arguments: For example (from
   the docs):

.. code:: python

      import argparse

      parser = argparse.ArgumentParser(description='Process some integers.')
      parser.add_argument('integers', metavar='N', type=int, nargs='+',
                          help='an integer for the accumulator')
      parser.add_argument('--sum', dest='accumulate', action='store_const',
                          const=sum, default=max,
                          help='sum the integers (default: find the max)')

      args = parser.parse_args()

3. Use verbosity to add and process the argparse a build the appropriate
   logging:

.. code:: python

      import logging
      import argparse
      import verbosity

      parser = argparse.ArgumentParser(description='Process some integers.')
      parser.add_argument('integers', metavar='N', type=int, nargs='+',
                          help='an integer for the accumulator')
      parser.add_argument('--sum', dest='accumulate', action='store_const',
                          const=sum, default=max,
                          help='sum the integers (default: find the max)')

      verbosity.add_arguments(parser)

      args = parser.parse_args()

      # initialize logging handle logging arguments
      verbosity.initialize(logger)
      verbosity.handle_arguments(args, logger)

Please use Github issues to report any bugs or request enhancements.
