Overlock Python client library |Build Status| |Pypi|
====================================================

The `Overlock`_ python library allows logging and instrumentation of
program code as a drop in replacement for python logging, but with some
extensions. Only for use with the Overlock Agent for linux.

See https://docs.overlock.io/libraries/python/ for instructions.

Python versions supported:

-  2.7
-  3.4
-  3.5
-  3.6
-  pypy
-  pypy3

Using the library
-----------------

The overlock library needs to be 'installed' in your code to configure
and provide some details to the Overlock Agent:

.. code:: python


    from overlock import install

    install(
        # The name of the application program, defaults to "unknown"
        process_name="sensor-reader", 
        # Any custom metadata for the app can be added here
        metadata={
            "version": "2.0.1",
            "hardware_revision": get_hardware_version()
        },
    )


When installed, it can be used to log information from all parts of your
system

.. code:: python

    from overlock import OverlockLogger
    ol = OverlockLogger() # 1 - Import the logger

    def read_sensor():
        try:
            value = read_sensor()
            ol.set_state({"sensor_value": value}) # 2 - Use set_state to add state to the store
            ol.info("got a new reading for the sensor") # 3a - Add a log message
            return value
        except SensorReadException as e:
            ol.set_state({"sensor_value": "unknown"})
            ol.exception("Error trying to get sensor value!") # 3b - Log an exception

Running tests
-------------

1. Install tox: ``pip install tox``
2. Run tests ``tox``

Note: you may want to comment out some of the python versions if your
system does not have them installed.

.. |Pypi| image:: https://img.shields.io/pypi/v/overlock.svg
   :target: https://pypi.python.org/pypi/overlock

.. _Overlock: https://overlock.io

.. |Build Status| image:: https://travis-ci.org/OverlockIoT/overlock-python.svg?branch=master
   :target: https://travis-ci.org/OverlockIoT/overlock-python