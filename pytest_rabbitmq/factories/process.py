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

from pathlib import Path
from typing import (
    Any,
    Callable,
    Generator,
    List,
    Optional,
    Set,
    Tuple,
    TypedDict,
    Union,
)
from warnings import warn

import pytest
from mirakuru.exceptions import ProcessExitedWithError
from port_for import get_port
from pytest import FixtureRequest, TempPathFactory

from pytest_rabbitmq.factories.executor import RabbitMqExecutor

PortType = Union[
    None,
    str,
    int,
    Tuple[int, int],
    Set[int],
    List[str],
    List[int],
    List[Tuple[int, int]],
    List[Set[int]],
    List[Union[Set[int], Tuple[int, int]]],
    List[Union[str, int, Tuple[int, int], Set[int]]],
]


class RabbitMQConfig(TypedDict):
    """Pytest RabbitMQ config definition type."""

    host: str
    port: PortType
    distribution_port: PortType
    logsdir: Optional[Path]
    server: str
    ctl: str
    node: str
    plugindir: Path


def get_config(request: FixtureRequest) -> RabbitMQConfig:
    """Return a dictionary with config options."""

    def get_conf_option(option: str) -> Any:
        option_name = "rabbitmq_" + option
        return request.config.getoption(option_name) or request.config.getini(option_name)

    port = get_conf_option("port")
    distribution_port = get_conf_option("distribution_port")
    logsdir = get_conf_option("logsdir")
    config: RabbitMQConfig = {
        "host": get_conf_option("host"),
        "port": int(port) if port else None,
        "distribution_port": int(distribution_port) if distribution_port else None,
        "logsdir": Path(logsdir) if logsdir else None,
        "server": get_conf_option("server"),
        "ctl": get_conf_option("ctl"),
        "node": get_conf_option("node"),
        "plugindir": Path(get_conf_option("plugindir")),
    }
    return config


def rabbitmq_proc(
    server: Optional[str] = None,
    host: Optional[str] = None,
    port: PortType = -1,
    distribution_port: PortType = -1,
    node: Optional[str] = None,
    ctl: Optional[str] = None,
    logsdir: Optional[Path] = None,
    plugindir: Optional[Path] = None,
) -> Callable[[FixtureRequest, TempPathFactory], Generator[RabbitMqExecutor, None, None]]:
    """Fixture factory for RabbitMQ process.

    :param server: path to rabbitmq-server command
    :param host: server host
    :param port:
        exact port (e.g. '8000', 8000)
        randomly selected port (None) - any random available port
        [(2000,3000)] or (2000,3000) - random available port from a given range
        [{4002,4003}] or {4002,4003} - random of 4002 or 4003 ports
        [(2000,3000), {4002,4003}] -random of given range and set
    :param distribution_port:
        exact port (e.g. '8000', 8000)
        randomly selected port (None) - any random available port
        [(2000,3000)] or (2000,3000) - random available port from a given range
        [{4002,4003}] or {4002,4003} - random of 4002 or 4003 ports
        [(2000,3000), {4002,4003}] -random of given range and set
    :param node: RabbitMQ node name used for setting environment
                          variable RABBITMQ_NODENAME (the default depends
                          on the port number, so multiple nodes are not
                          clustered)
    :param ctl: path to rabbitmqctl file
    :param logsdir: path to log directory

    :returns pytest fixture with RabbitMQ process executor
    """

    @pytest.fixture(scope="session")
    def rabbitmq_proc_fixture(
        request: FixtureRequest, tmp_path_factory: TempPathFactory
    ) -> Generator[RabbitMqExecutor, None, None]:
        """Fixture for RabbitMQ process.

        #. Get config.
        #. Make a temporary directory.
        #. Setup required environment variables:
        #.  * RABBITMQ_LOG_BASE
        #.  * RABBITMQ_MNESIA_BASE
        #.  * RABBITMQ_ENABLED_PLUGINS_FILE
        #.  * RABBITMQ_NODE_PORT
        #.  * RABBITMQ_DIST_PORT
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
        assert rabbit_port
        rabbit_distribution_port = get_port(distribution_port, [rabbit_port]) or get_port(
            config["distribution_port"], [rabbit_port]
        )
        assert rabbit_distribution_port
        assert (
            rabbit_distribution_port != rabbit_port
        ), "rabbit_port and distribution_port can not be the same!"

        tmpdir = tmp_path_factory.mktemp(f"pytest-rabbitmq-{request.fixturename}")

        rabbit_plugin_path = plugindir or config["plugindir"]

        rabbit_logpath = config["logsdir"] or logsdir
        if rabbit_logpath:
            warn(
                f"rabbitmq_logsdir and --rabbitmq-logsdir config option is "
                f"deprecated, and will be dropped in future releases. "
                f"All fixture related data resides within {tmpdir}",
                DeprecationWarning,
            )
        if not rabbit_logpath:
            rabbit_logpath = tmpdir / "logs"

        rabbit_executor = RabbitMqExecutor(
            rabbit_server,
            rabbit_host,
            rabbit_port,
            rabbit_distribution_port,
            rabbit_ctl,
            logpath=rabbit_logpath,
            path=tmpdir,
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
