.. image:: https://travis-ci.org/USGS-EROS/lcmap-merlin.svg?branch=develop
    :target: https://travis-ci.org/USGS-EROS/lcmap-merlin

.. image:: https://readthedocs.org/projects/lcmap-merlin/badge/?version=latest
    :target: http://lcmap-merlin.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/lcmap-merlin.svg
    :target: https://pypi.python.org/pypi/lcmap-merlin/


Merlin
======
A Python3 library for turning LCMAP spatial data into timeseries like magic.

Features
--------
* Retrieve chips & chip specs
* Convert chips & chip specs into time series rods
* Many composable functions
* Works with symmetric or assymetric data arrays
* Built with efficiency in mind... leverages Numpy for heavy lifting.
* Tested with cPython 3.5 & 3.6


Example
-------
.. code-block:: python3

    import merlin

    timeseries = merlin.create(x=123,
                               y=456,
                               acquired='1980-01-01/2017-01-01',
                               cfg=merlin.cfg.get(profile='chipmunk-ard',
                                                  env={'CHIPMUNK_URL': 'http://localhost:5656'}))

    print(timeseries)

    (((123, 456, 123, 456), {'reds'  : [9, 8, ...],
                             'greens': [99, 88, ...]},
                             'blues' : [12, 22, ...],
                             'dates':  ['2017-01-01', '2016-12-31', ...]}),
     ((123, 456, 124, 456), {'reds'  : [4, 3, ...],
                             'greens': [19, 8, ...]},
                             'blues' : [1, 11, ...],
                             'dates':  ['2017-01-01', '2016-12-31', ...]}),)


Documentation
-------------
Complete documentation is available at http://lcmap-merlin.readthedocs.io/


Installation
------------

.. code-block:: bash

   pip install lcmap-merlin


Versioning
----------
Merlin follows semantic versioning: http://semver.org/

License
-------
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to http://unlicense.org.
