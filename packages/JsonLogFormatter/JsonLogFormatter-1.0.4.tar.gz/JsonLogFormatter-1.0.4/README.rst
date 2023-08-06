Json log formatter
=======================

.. image:: https://travis-ci.org/ObadaAlexandru/JsonLogFormatter.svg?branch=master
    :target: https://travis-ci.org/ObadaAlexandru/JsonLogFormatter

Formats the log messages in a JSON format as follows:

.. code-block:: javascript

        {   "description": "Some exception",
             "log_type": "application_log"
             "severity": "ERROR",
             "source_file": "test.py",
             "module": "test",
             "thread": "MainThread",
             "pid": 74607,
             "stacktrace": "Traceback (most recent call last):\n  File\"test.py\", line 20,"
         }


A message in JSON format facilitates the logs processing.