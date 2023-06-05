# Copyright (C) 2014 by Clearcode <http://clearcode.cc>
# and associates (see AUTHORS).

# This file is part of pytest-rabbitmq.

# pytest-rabbitmq is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pytest-rabbitmq is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with pytest-rabbitmq.  If not, see <http://www.gnu.org/licenses/>.
"""RabbitMQ process fixture factory."""

import os
from tempfile import gettempdir

import pytest
from mirakuru.exceptions import ProcessExitedWithError
from port_for import get_port

from pytest_rabbitmq.factories.executor import RabbitMqExecutor


def get_config(request):
    """Return a dictionary with config options."""
    config = {}
    options = ["logsdir", "host", "port", "server", "ctl", "node", "plugindir"]
    for option in options:
        option_name = "rabbitmq_" + option
        conf = request.config.getoption(option_name) or request.config.getini(option_name)
        config[option] = conf
    return config


def rabbitmq_proc(
    server=None,
    host=None,
    port=-1,
    node=None,
    ctl=None,
    logsdir=None,
    plugindir=None,
):
    """
    Fixture factory for RabbitMQ process.

    :param str server: path to rabbitmq-server command
    :param str host: server host
    :param str|int|tuple|set|list port:
        exact port (e.g. '8000', 8000)
        randomly selected port (None) - any random available port
        [(2000,3000)] or (2000,3000) - random available port from a given range
        [{4002,4003}] or {4002,4003} - random of 4002 or 4003 ports
        [(2000,3000), {4002,4003}] -random of given range and set
    :param str node: RabbitMQ node name used for setting environment
                          variable RABBITMQ_NODENAME (the default depends
                          on the port number, so multiple nodes are not
                          clustered)
    :param str ctl: path to rabbitmqctl file
    :param str logsdir: path to log directory

    :returns pytest fixture with RabbitMQ process executor
    """

    @pytest.fixture(scope="session")
    def rabbitmq_proc_fixture(request):
        """
        Fixture for RabbitMQ process.

        #. Get config.
        #. Make a temporary directory.
        #. Setup required environment variables:
        #.  * RABBITMQ_LOG_BASE
        #.  * RABBITMQ_MNESIA_BASE
        #.  * RABBITMQ_ENABLED_PLUGINS_FILE
        #.  * RABBITMQ_NODE_PORT
        #.  * RABBITMQ_NODENAME
        #. Start a rabbit server
            `<http://www.rabbitmq.com/man/rabbitmq-server.1.man.html>`_
        #. Stop rabbit server and remove temporary files after tests.

        :param FixtureRequest request: fixture request object
        :rtype: pytest_rabbitmq.executors.TCPExecutor
        :returns: tcp executor of running rabbitmq-server
        """
        config = get_config(request)
        rabbit_ctl = ctl or config["ctl"]
        rabbit_server = server or config["server"]
        rabbit_host = host or config["host"]
        rabbit_port = get_port(port) or get_port(config["port"])

        rabbit_path = os.path.join(gettempdir(), f"rabbitmq.{rabbit_port}/")
        rabbit_plugin_path = plugindir or config["plugindir"] or rabbit_path

        rabbit_executor = RabbitMqExecutor(
            rabbit_server,
            rabbit_host,
            rabbit_port,
            rabbit_ctl,
            logpath=config["logsdir"] or logsdir,
            path=rabbit_path,
            plugin_path=rabbit_plugin_path,
            node_name=node or config["node"],
        )

        rabbit_executor.start()
        yield rabbit_executor
        try:
            rabbit_executor.stop()
        except ProcessExitedWithError:
            pass

    return rabbitmq_proc_fixture
