sen14348_exporter
=================

Python Prometheus exporter for the SparkFun Environmental Combo Breakout
(SEN-14348)

Requirements
------------

-  `bme280_exporter <https://github.com/ashtreefarms/bme280-exporter>`__
-  `ccs811_exporter <https://github.com/ashtreefarms/ccs811-exporter>`__

Installation
------------

.. code:: bash

    pip install sen14348_exporter

Usage
-----

.. code:: bash

    $ sen14348_exporter -h
    usage: sen14348_exporter [-h] [-v] [-p PORT] [-ba BME_ADDRESS]
                             [-ca CCS_ADDRESS] [-l LABELS] [-i INTERVAL]
                             [-bf FILTER] [-bho BHO] [-bpo BPO] [-bto BTO]
                             [-cto CTO]

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         increase output verbosity
      -p PORT, --port PORT  exporter port (default: 9502)
      -ba BME_ADDRESS, --bme-address BME_ADDRESS
                            BME280 I2C address (default: 0x77)
      -ca CCS_ADDRESS, --ccs-address CCS_ADDRESS
                            CCS811 I2C address (default: 0x5b)
      -l LABELS, --labels LABELS
                            JSON object of Prometheus labels to apply
      -i INTERVAL, --interval INTERVAL
                            measurement sample interval (default: 2)
      -bf FILTER, --filter FILTER
                            BME280 filter value to apply (0-4, default: 0)
      -bho BHO              BME280 humidity oversampling value (1-5, default: 4)
      -bpo BPO              BME280 pressure oversampling value (1-5, default: 4)
      -bto BTO              BME280 temperature oversampling value (1-5, default:
                            4)
      -cto CTO              CCS811 temperature offset (default: -25.0)

Docker
------

.. code:: bash

    docker pull ashtreefarms/sen14348-exporter-rpi
    docker run -p 9502:9502 --device /dev/i2c-1 ashtreefarms/sen14348-exporter-rpi \
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
