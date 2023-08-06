pine
====

A benchmark utility to make requests to a REST API.

Pine makes requests to URLs a bunch of times and computes some statistics
about how those requests were responded to. This is ideally useful to run
on every change to your codebase so you can identify changes early.

Pine isn't a load testing tool. If you're trying to solve C10K, this won't
help you. Pine (currently) runs requests serially.

Usage
=====

``pine -c myconfig.yaml`` is the simplest way to begin. This will run your
configuration and output the results to stdout. If you'd like to write
the output to a file, ``-o myoutputfile.json`` will do it. If you'd like
to specify a particular run ID, other than the default of the current
timestamp, ``-i 32a63ab`` will do it. That's useful for tracking the
commit hash of what you're testing.

Run ``pine -h`` for complete details.

Configuration
=============

Pine uses YAML for configuration. See
`conf/example.yaml <https://github.com/briancurtin/pine/blob/master/conf/example.yaml>`_
for an example.

Output
======

Pine writes its results in JSON, either to stdout or the path you specified
in ``-o``. It looks like the following::

    {"results": [
        {"timeouts": 0, "failures": [], "name": "get_all_things",
         "description": "Get all of the things", "version": "1.0",
         "mean": 1.668359371049998,
         "median": 1.580882219500005,
         "stdev": 0.0969358463985873},
        {"timeouts": 0, "failures": [], "name": "get_one_thing",
         "description": "Get one thing", "version": "1.0",
         "mean": 0.856881387399993,
         "median": 0.508042131499991,
         "stdev": 0.0646515285845596},
     ],
     "id": "7155eb"}

Requirements
============

Pine uses aiohttp on Python 3.7.

Thanks
======

Thanks to Francis Horsman for the ``pine`` package name.
