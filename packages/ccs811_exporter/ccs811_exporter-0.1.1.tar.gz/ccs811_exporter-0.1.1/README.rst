ccs811_exporter
===============

Python Prometheus exporter for the ams CCS811 sensor

Requirements
------------

-  `Adafruit_CCS811_Python <https://github.com/adafruit/Adafruit_CCS811_Python>`__

Installation
------------

.. code:: bash

    pip install ccs811_exporter

Usage
-----

.. code:: bash

    $ ccs811_exporter -h
    usage: ccs811_exporter [-h] [-v] [-p PORT] [-a ADDRESS] [-l LABELS]
                           [-i INTERVAL] [-to TO]

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         increase output verbosity
      -p PORT, --port PORT  exporter port (default: 9501)
      -a ADDRESS, --address ADDRESS
                            CCS811 I2C address (default: 0x5b
      -l LABELS, --labels LABELS
                            JSON object of Prometheus labels to apply
      -i INTERVAL, --interval INTERVAL
                            measurement sample interval (default: 2)
      -to TO                temperature offset (default: -25.00

Docker
------

.. code:: bash

    docker pull ashtreefarms/ccs811-exporter-rpi
    docker run -p 9501:9501 --device /dev/i2c-1 ashtreefarms/ccs811-exporter-rpi \
               --labels '{"zone": "bedroom"}'

MIT License
===========

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
