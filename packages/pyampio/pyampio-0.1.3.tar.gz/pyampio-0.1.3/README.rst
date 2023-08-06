|Build Status| |PyPI Version|

Python AMPIO Home Server Client
===============================

Python Client to AMPIO Home Server

Requires Python 3.4+

Installation
------------

.. code:: shell

   $ python setup.py install


Testing
-------

.. code:: shell

   $ ampio --help
   Usage: ampio [OPTIONS]

   Options:
     --port PATH                     The USB interface full path i.e.
                                     /dev/cu.usbserial-DN01D1W1. If no --port
                                     option provided the AMPIO_PORT environment
                                     variable is used.  [required]
     --log-level [NONE|DEBUG|INFO|ERROR]
                                     Logging level.  [default: ERROR]
     --help                          Show this message and exit.

   $ ampio --port /dev/dev/cu.usbserial-DN01D1W1


.. |Build Status| image:: https://travis-ci.org/kstaniek/pyampio.svg
   :target: https://travis-ci.org/kstaniek/pyampio
.. |PyPI Version| image:: https://img.shields.io/pypi/v/pyampio.svg
   :target: https://pypi.org/project/pyampio/
