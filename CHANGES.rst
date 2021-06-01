CHANGELOG
=========

unreleased
----------

Misc
++++

- Migrate CI to github actions
- Extended range of messages for list queues output
- Support only python 3.7 and up

2.1.0
----------

Feature
+++++++
- Allow to configure plugin's location with the use of

  * **--rabbitmq-logsdir** command line argument
  * **rabbitmq_logsdir** ini file configuration option
  * **logsdir** factory argument

2.0.1
----------

- [fix] Adjust for mirakuru 2.2.0 and up

2.0.0
----------

- [cleanup] Move more rabbitmq related logic into the executor
- [enhancements] Base environment variables support on the mirakuru functionality itself
- [feature] Drop support for python 2.7. From now on, only support python 3.6 and up

1.1.2
----------

- [fix] Fix list queues functionality

1.1.1
----------

- [enhancemet] removed path.py dependency

1.1.0
----------

- [enhancements] adjust pytest-rabbitmq to pytest 3. require pytest 3.

1.0.0
----------

- [enhancements] command line and pytest.ini options for modifying rabbitmq node name
- [enhancements] command line and pytest.ini options for modifying server exec path
- [enhancements] command line and pytest.ini options for modifying ctl exec path
- [enhancements] command line and pytest.ini options for modifying host
- [enhancements] command line and pytest.ini options for modifying port
- [enhancements] command line and pytest.ini options for modifying logs directory destination
