Json log formatter
=======================

.. image:: https://travis-ci.org/ObadaAlexandru/JsonLogFormatter.svg?branch=master
    :target: https://travis-ci.org/ObadaAlexandru/JsonLogFormatter

Formats the log messages in a JSON format as follows:
.. highlight:: json
::
 {   "description": "Some exception",
     "log_type": "application_log"
     "severity": "ERROR",
     "source_file": "test.py",
     "module": "test",
     "thread": "MainThread",
     "pid": 74607,
     "stacktrace": "Traceback (most recent call last):\n  File
 \"test.py\", line 20, in <module>\n    throw_exception()\n  File \"/test.py\", line 15, in throw_exception\nraise ValueError('Some exception')\nValueError: Some exception",
    "@timestamp": "2018-03-07T00:00:38.516213"}


A message in JSON format facilitates the logs processing.