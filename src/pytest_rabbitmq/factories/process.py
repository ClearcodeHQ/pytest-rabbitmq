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
import subprocess
from tempfile import gettempdir

import pytest
from mirakuru import TCPExecutor

from pytest_rabbitmq.port import get_port


def get_config(request):
    """Return a dictionary with config options."""
    config = {}
    options = [
        'logsdir', 'host', 'port', 'server', 'ctl', 'node'
    ]
    for option in options:
        option_name = 'rabbitmq_' + option
        conf = request.config.getoption(option_name) or \
            request.config.getini(option_name)
        config[option] = conf
    return config


class RabbitMqExecutor(TCPExecutor):
    """RabbitMQ executor to start specific rabbitmq instances."""

    def __init__(self, command, host, port, rabbit_ctl, environ, **kwargs):
        """
        Initialize RabbitMQ executor.

        :param str command: rabbitmq-server location
        :param str host: host where rabbitmq will be accessible
        :param int port: port under which rabbitmq runs
        :param str rabbit_ctl: rabbitctl location
        :param dict environ: rabbitmq configuration environment variables
        :param kwargs: see TCPExecutor for description
        """
        super(RabbitMqExecutor, self).__init__(
            command, host, port, timeout=60, **kwargs
        )
        self.rabbit_ctl = rabbit_ctl
        self.env = environ

    def set_environ(self):
        """Update RabbitMQ enviroment variables for configuration."""
        os.environ.update(self.env)

    def start(self):
        """Start RabbitMQ."""
        self.set_environ()
        TCPExecutor.start(self)

    def rabbitctl_output(self, *args):
        """
        Query rabbitctl with args.

        :param list args: list of additional args to query
        """
        self.set_environ()
        ctl_command = [self.rabbit_ctl]
        ctl_command.extend(args)
        return subprocess.check_output(ctl_command).decode('utf-8')

    def list_exchanges(self):
        """Get exchanges defined on given rabbitmq."""
        exchanges = []
        output = self.rabbitctl_output('list_exchanges', 'name')
        unwanted_exchanges = ['Listing exchanges ...', '...done.']

        for exchange in output.split('\n'):
            if exchange and exchange not in unwanted_exchanges:
                exchanges.append(str(exchange))

        return exchanges

    def list_queues(self):
        """Get queues defined on given rabbitmq."""
        queues = []
        output = self.rabbitctl_output('list_queues', 'name')
        unwanted_queues = ['listing queues', 'done']

        for queue in output.split('\n'):
            if queue and queue.strip('. ').lower() not in unwanted_queues:
                queues.append(str(queue))

        return queues


def rabbitmq_proc(
        server=None, host=None, port=-1,
        node=None, ctl=None, logsdir=None, logs_prefix=''
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
    :param str logs_prefix: prefix for log directory

    :returns pytest fixture with RabbitMQ process executor
    """
    @pytest.fixture(scope='session')
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
        rabbit_ctl = ctl or config['ctl']
        rabbit_server = server or config['server']
        rabbit_host = host or config['host']
        rabbit_port = get_port(port) or get_port(config['port'])

        rabbit_path = os.path.join(
            gettempdir(),
            f'rabbitmq.{rabbit_port}/'
        )

        rabbit_log = os.path.join(
            (config['logsdir'] or logsdir),
            f'{logs_prefix}rabbit-server.{rabbit_port}.log'
        )

        rabbit_mnesia = rabbit_path + 'mnesia'
        rabbit_plugins = rabbit_path + 'plugins'

        # Use the port number in node name, so multiple instances started
        # at different ports will work separately instead of clustering.
        chosen_node_name = node or config['node'] \
            or f'rabbitmq-test-{rabbit_port}'

        environ = {
            'RABBITMQ_LOG_BASE': rabbit_log,
            'RABBITMQ_MNESIA_BASE': rabbit_mnesia,
            'RABBITMQ_ENABLED_PLUGINS_FILE': rabbit_plugins,
            'RABBITMQ_NODE_PORT': str(rabbit_port),
            'RABBITMQ_NODENAME': chosen_node_name,
        }

        rabbit_executor = RabbitMqExecutor(
            rabbit_server,
            rabbit_host,
            rabbit_port,
            rabbit_ctl,
            environ
        )

        request.addfinalizer(rabbit_executor.stop)

        rabbit_executor.start()

        return rabbit_executor

    return rabbitmq_proc_fixture
