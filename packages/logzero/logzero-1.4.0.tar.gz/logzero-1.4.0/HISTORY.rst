=======
History
=======

1.3.1 (2018-03-02)
------------------
* Allow Disabling stderr Output (`PR 83 <https://github.com/metachris/logzero/pull/83>`_)


1.3.0 (2017-07-19)
------------------

* Color output now works in Windows (supported by colorama)


1.2.1 (2017-07-09)
------------------

* Logfiles with custom loglevels (eg. stream handler with DEBUG and file handler with ERROR).


1.2.0 (2017-07-05)
------------------

* Way better API for configuring the default logger with `logzero.loglevel(..)`, `logzero.logfile(..)`, etc.
* Built-in rotating logfile support.

.. code-block:: python

    import logging
    import logzero
    from logzero import logger

    # This log message goes to the console
    logger.debug("hello")

    # Set a minimum log level
    logzero.loglevel(logging.INFO)

    # Set a logfile (all future log messages are also saved there)
    logzero.logfile("/tmp/logfile.log")

    # Set a rotating logfile (replaces the previous logfile handler)
    logzero.logfile("/tmp/rotating-logfile.log", maxBytes=1000000, backupCount=3)

    # Disable logging to a file
    logzero.logfile(None)

    # Set a custom formatter
    formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s');
    logzero.formatter(formatter)

    # Log some variables
    logger.info("var1: %s, var2: %s", var1, var2)


1.1.2 (2017-07-04)
------------------

* Better reconfiguration of handlers, doesn't remove custom handlers anymore


1.1.0 (2017-07-03)
------------------

* Bugfix: Disabled color logging to logfile


1.1.0 (2017-07-02)
------------------

* Global default logger instance (`logzero.logger`)
* Ability to reconfigure the default logger with (`logzero.setup_default_logger(..)`)
* More tests
* More documentation

1.0.0 (2017-06-27)
------------------

* Cleanup and documentation


0.2.0 (2017-06-12)
------------------

* Working logzero package with code and tests


0.1.0 (2017-06-12)
------------------

* First release on PyPI.
