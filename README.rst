.. image:: https://raw.githubusercontent.com/ClearcodeHQ/pytest-rabbitmq/master/logo.png
    :width: 100px
    :height: 100px
    
pytest-rabbitmq
===============

.. image:: https://img.shields.io/pypi/v/pytest-rabbitmq.svg
    :target: https://pypi.python.org/pypi/pytest-rabbitmq/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/wheel/pytest-rabbitmq.svg
    :target: https://pypi.python.org/pypi/pytest-rabbitmq/
    :alt: Wheel Status

.. image:: https://img.shields.io/pypi/pyversions/pytest-rabbitmq.svg
    :target: https://pypi.python.org/pypi/pytest-rabbitmq/
    :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/pytest-rabbitmq.svg
    :target: https://pypi.python.org/pypi/pytest-rabbitmq/
    :alt: License

Package status
--------------

.. image:: https://travis-ci.org/ClearcodeHQ/pytest-rabbitmq.svg?branch=v2.2.1
    :target: https://travis-ci.org/ClearcodeHQ/pytest-rabbitmq
    :alt: Tests

.. image:: https://coveralls.io/repos/ClearcodeHQ/pytest-rabbitmq/badge.png?branch=v2.2.1
    :target: https://coveralls.io/r/ClearcodeHQ/pytest-rabbitmq?branch=v2.2.1
    :alt: Coverage Status

What is this?
=============

This is a pytest plugin, that enables you to test your code that relies on a running RabbitMQ Queues.
It allows you to specify additional fixtures for RabbitMQ process and client.

How to use
==========

Plugin contains two fixtures

* **rabbitmq** - it's a client fixture that has functional scope. After each test, it cleans RabbitMQ, cleans queues and exchanges for more reliable tests.
* **rabbitmq_proc** - session scoped fixture, that starts RabbitMQ instance at it's first use and stops at the end of the tests.

Simply include one of these fixtures into your tests fixture list.

You can also create additional rabbitmq client and process fixtures if you'd need to:


.. code-block:: python

    from pytest_rabbitmq import factories

    rabbitmq_my_proc = factories.rabbitmq_proc(
        port=None, logsdir='/tmp')
    rabbitmq_my = factories.rabbitmq('rabbitmq_my_proc')

.. note::

    Each RabbitMQ process fixture can be configured in a different way than the others through the fixture factory arguments.

Configuration
=============

You can define your settings in three ways, it's fixture factory argument, command line option and pytest.ini configuration option.
You can pick which you prefer, but remember that these settings are handled in the following order:

    * ``Fixture factory argument``
    * ``Command line option``
    * ``Configuration option in your pytest.ini file``

.. list-table:: Configuration options
   :header-rows: 1

   * - RabbitMQ option
     - Fixture factory argument
     - Command line option
     - pytest.ini option
     - Default
   * - host
     - host
     - --rabbitmq-host
     - rabbitmq_host
     - 127.0.0.1
   * - port
     - port
     - --rabbitmq-port
     - rabbitmq_port
     - random
   * - rabbitmqctl path
     - ctl
     - --rabbitmq-ctl
     - rabbitmq_ctl
     - /usr/lib/rabbitmq/bin/rabbitmqctl
   * - rabbitmq server path
     - server
     - --rabbitmq-server
     - rabbitmq_server
     - /usr/lib/rabbitmq/bin/rabbitmq-server
   * - Log directory location
     - logsdir
     - --rabbitmq-logsdir
     - rabbitmq_logsdir
     - $TMPDIR
   * - Plugin directory location
     - plugin_path
     - --rabbitmq-plugindir
     - rabbitmq_plugindir
     - $TMPDIR
   * - Node name
     - node
     - --rabbitmq-node
     - rabbitmq_node
     - rabbitmq-test-{port}


Example usage:

* pass it as an argument in your own fixture

    .. code-block:: python

        rabbitmq_proc = factories.rabbitmq_proc(port=8888)

* use ``--rabbitmq-port`` command line option when you run your tests

    .. code-block::

        py.test tests --rabbitmq-port=8888


* specify your port as ``rabbitmq_port`` in your ``pytest.ini`` file.

    To do so, put a line like the following under the ``[pytest]`` section of your ``pytest.ini``:

    .. code-block:: ini

        [pytest]
        rabbitmq_port = 8888

Package resources
-----------------

* Bug tracker: https://github.com/ClearcodeHQ/pytest-rabbitmq/issues
