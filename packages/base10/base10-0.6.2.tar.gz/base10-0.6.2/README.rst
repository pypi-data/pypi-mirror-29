Base10 |Version| |Build| |Coverage| |Health| |Docs| |CLA|
===================================================================

|Compatibility| |Implementations| |Format| |Downloads|

Base10 is a metrics abstractoin layer for linking multiple metrics source and stores. It also simplifies metric creation and proxying.


Documentation
-------------
Base10's documentation can be found at `https://base10.readthedocs.io <https://base10.readthedocs.io>`_


Installing Base10
-----------------
Base10 can be installed from Pypi using pip::

    pip install base10


Example
-------
This shows a simple metric generator that writes a JSON formatted metric, containing a random value, to RabbitMQ.

.. code :: python

    from random import random
    from time import sleep

    from base10 import MetricHelper, MetricHandler
    from base10.dialects import JSONDialect
    from base10.transports import RabbitMQWriter

    if __name__ == '__main__':

        class MyMetric(MetricHelper):
            _name = 'metric'

            _fields = [
                'value',
            ]

            _metadata = [
                'hostname',
            ]

        class JSON(MetricHandler):
            _dialect = JSONDialect()
            _writer = RabbitMQWriter(
                broker='127.0.0.1', exchange='amq.topic', topic='metrics.example')

        json = JSON()

        while True:
            json.write(MyMetric(value=random(), hostname='test'))
            sleep(1)

This shows a simple proxy that reads JSON formatted metrics from RabbitMQ and outputs them in InfluxDB format over a UDP socket.

.. code :: python

    from base10 import MetricHandler
    from base10.dialects import JSONDialect, SplunkDialect  #InfluxDBDialect
    from base10.transports import RabbitMQReader, UDPWriter

    if __name__ == '__main__':

        class RabbitMQ(MetricHandler):
            _dialect = JSONDialect()
            _reader = RabbitMQReader(
                broker='127.0.0.1', exchange='amq.topic', routing_key='metrics.#')

        class InfluxDB(MetricHandler):
            _dialect = SplunkDialect()  #InfluxDBDialect()
            _writer = UDPWriter(host='127.0.0.1', port=10000)

        rabbitmq = RabbitMQ()
        influxdb = InfluxDB()

        for metric in rabbitmq.read():
            influxdb.write(metric)


Contributing
------------
To contribute to base10, please make sure that any new features or changes
to existing functionality **include test coverage**.

*Pull requests that add or change code without coverage will most likely be rejected.*

Additionally, please format your code using `yapf <http://pypi.python.org/pypi/yapf>`_
with ``facebook`` style prior to issuing your pull request.

``yapf --style=facebook -i -r base10 setup.py``


.. |Build| image:: https://travis-ci.org/mattdavis90/base10.svg?branch=master
   :target: https://travis-ci.org/mattdavis90/base10
.. |Coverage| image:: https://img.shields.io/coveralls/mattdavis90/base10.svg
   :target: https://coveralls.io/r/mattdavis90/base10
.. |Health| image:: https://codeclimate.com/github/mattdavis90/base10/badges/gpa.svg
   :target: https://codeclimate.com/github/mattdavis90/base10
.. |Version| image:: https://img.shields.io/pypi/v/base10.svg
   :target: https://pypi.python.org/pypi/base10
.. |Docs| image:: https://readthedocs.org/projects/base10/badge/?version=latest
   :target: https://base10.readthedocs.io
.. |CLA| image:: https://cla-assistant.io/readme/badge/mattdavis90/base10
   :target: https://cla-assistant.io/mattdavis90/base10
.. |Downloads| image:: https://img.shields.io/pypi/dm/base10.svg
   :target: https://pypi.python.org/pypi/base10
.. |Compatibility| image:: https://img.shields.io/pypi/pyversions/base10.svg
   :target: https://pypi.python.org/pypi/base10
.. |Implementations| image:: https://img.shields.io/pypi/implementation/base10.svg
   :target: https://pypi.python.org/pypi/base10
.. |Format| image:: https://img.shields.io/pypi/format/base10.svg
   :target: https://pypi.python.org/pypi/base10
