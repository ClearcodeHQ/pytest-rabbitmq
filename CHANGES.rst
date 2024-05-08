CHANGELOG
=========

.. towncrier release notes start

3.1.0 (2024-05-08)
==================

Features
--------

- Support Python 3.12 (`#469 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/469>`_)


Miscellaneus
------------

- Update code formatting with black 24.1 (`#424 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/424>`_)
- Drop Pipfile.lock from repository - rely on a cached/artifacted one. (`#468 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/468>`_)


3.0.2 (2023-07-05)
==================

Bugfixes
--------

- Fixes logdir config option reading. (`#354 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/354>`_)
- Fixes type hints for specifying ports in Rabbitmq startup process. (`#355 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/355>`_)


3.0.1 (2023-06-16)
==================

Bugfixes
--------

- Fixed rabbitmq entrypoint (`#349 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/349>`_)


3.0.0 (2023-06-15)
==================

Breaking changes
----------------

- Add your info here (`#313 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/313>`_)
- Dropped support for Python 3.7 (`#324 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/324>`_)


Deprecations
------------

- Deprecate `rabbitmq_logsdir` and `--rabbitmq-logsdir` config options. (`#266 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/266>`_)


Features
--------

- Use `tmp_path_factory` instead of gettempdir() manually.
  This will allow cleaning of a temporary files. (`#266 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/266>`_)
- Define RABBITMQ_DIST_PORT for rabbitmq.
  Added `--rabbitmq-distribution-port` to commandline and `rabbitmq_distribution_port` to ini configuration options.

  This will help both with macos port number limit (as by default Rabbitmk adds 20000 to the Node port to determine the port), and the port being already used error.

  This port has to be different that rabbitmq port. (`#317 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/317>`_)
- Use towncrier to manage changelog. Require Pull Requests to contain proper newsfragment. (`#319 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/319>`_)
- Introduce typing and run mypy checks (`#324 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/324>`_)
- Official Python 3.11 support (`#329 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/329>`_)


Miscellaneus
------------

- Upadte test pipeline to install fresh rabbitmq from apt. (`#280 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/280>`_)
- Migrate dev dependency management to pipfile (`#320 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/320>`_)
- Migrate automerge workflow to shared one with merger app (`#321 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/321>`_)
- Replace pycodestyle and pydocstyle with ruff. (`#322 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/322>`_)
- Move package configuration to pyproject.toml (`#323 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/323>`_)
- Migrate to tbump to manage package versions (`#340 <https://github.com/ClearcodeHQ/pytest-rabbitmq/issues/340>`_)


2.2.1
=====

Bugfix
------

- require `port-for>=0.6.0` which introduced the `get_port` function

Misc
----

- updated trove classifiers - added python 3.10 and pypy

2.2.0
=====

Bugfix
------

- rely on `get_port` functionality delivered by `port_for`
- Extended range of messages for list queues output

Misc
++++

- Migrate CI to github actions
- Support only python 3.7 and up

2.1.0
=====

Feature
-------
- Allow to configure plugin's location with the use of

  * **--rabbitmq-logsdir** command line argument
  * **rabbitmq_logsdir** ini file configuration option
  * **logsdir** factory argument

2.0.1
=====

- [fix] Adjust for mirakuru 2.2.0 and up

2.0.0
=====

- [cleanup] Move more rabbitmq related logic into the executor
- [enhancements] Base environment variables support on the mirakuru functionality itself
- [feature] Drop support for python 2.7. From now on, only support python 3.6 and up

1.1.2
=====

- [fix] Fix list queues functionality

1.1.1
=====

- [enhancemet] removed path.py dependency

1.1.0
=====

- [enhancements] adjust pytest-rabbitmq to pytest 3. require pytest 3.

1.0.0
=====

- [enhancements] command line and pytest.ini options for modifying rabbitmq node name
- [enhancements] command line and pytest.ini options for modifying server exec path
- [enhancements] command line and pytest.ini options for modifying ctl exec path
- [enhancements] command line and pytest.ini options for modifying host
- [enhancements] command line and pytest.ini options for modifying port
- [enhancements] command line and pytest.ini options for modifying logs directory destination
