# Copyright (C) 2013 by Clearcode <http://clearcode.cc>
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
"""Plugin definition for pytest-rabbitmq."""
from tempfile import gettempdir

from pytest_rabbitmq import factories


# pylint:disable=invalid-name
_help_ctl = "RabbitMQ ctl path"
_help_server = "RabbitMQ server path"
_help_logsdir = "Logs directory location"
_help_plugindir = "Directory where 'plugin' file is located"
_help_host = "Host at which RabbitMQ will accept connections"
_help_port = "Port at which RabbitMQ will accept connections"
_help_node = "Node name for rabbitmq instance"


def pytest_addoption(parser):
    """Confioguration option."""
    parser.addini(name="rabbitmq_host", help=_help_host, default="127.0.0.1")
    parser.addini(
        name="rabbitmq_port",
        help=_help_port,
        default=None,
    )
    parser.addini(
        name="rabbitmq_ctl",
        help=_help_ctl,
        default="/usr/lib/rabbitmq/bin/rabbitmqctl",
    )
    parser.addini(
        name="rabbitmq_server",
        help=_help_server,
        default="/usr/lib/rabbitmq/bin/rabbitmq-server",
    )
    parser.addini(
        name="rabbitmq_logsdir",
        help=_help_logsdir,
        default=gettempdir(),
    )
    parser.addini(
        name="rabbitmq_plugindir",
        help=_help_logsdir,
        default=gettempdir(),
    )
    parser.addini(
        name="rabbitmq_node",
        help=_help_node,
        default=None,
    )

    parser.addoption(
        "--rabbitmq-host",
        action="store",
        dest="rabbitmq_host",
        help=_help_host,
    )
    parser.addoption("--rabbitmq-port", action="store", dest="rabbitmq_port", help=_help_port)
    parser.addoption("--rabbitmq-ctl", action="store", dest="rabbitmq_ctl", help=_help_ctl)
    parser.addoption("--rabbitmq-server", action="store", dest="rabbitmq_server", help=_help_server)
    parser.addoption(
        "--rabbitmq-logsdir",
        action="store",
        metavar="path",
        dest="rabbitmq_logsdir",
        help=_help_logsdir,
    )
    parser.addoption(
        "--rabbitmq-plugindir",
        action="store",
        metavar="path",
        dest="rabbitmq_plugindir",
        help=_help_plugindir,
    )
    parser.addoption(
        "--rabbitmq-node",
        action="store",
        dest="rabbitmq_node",
        help=_help_node,
    )


rabbitmq_proc = factories.rabbitmq_proc()
rabbitmq = factories.rabbitmq("rabbitmq_proc")
