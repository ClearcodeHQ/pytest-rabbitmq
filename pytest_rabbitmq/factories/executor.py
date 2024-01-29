"""RabbitMQ Executor."""

import re
import subprocess
from pathlib import Path
from typing import List, Optional

from mirakuru import TCPExecutor


class RabbitMqExecutor(TCPExecutor):
    """RabbitMQ executor to start specific rabbitmq instances."""

    _UNWANTED_QUEUE_PATTERN = re.compile("(done|timeout:|listing queues)")

    def __init__(
        self,
        command: str,
        host: str,
        port: int,
        distribution_port: int,
        rabbit_ctl: str,
        logpath: Path,
        path: Path,
        plugin_path: Path,
        node_name: Optional[str] = None,
    ) -> None:  # pylint:disable=too-many-arguments
        """Initialize RabbitMQ executor.

        :param command: rabbitmq-server location
        :param host: host where rabbitmq will be accessible
        :param port: port under which rabbitmq runs
        :param rabbit_ctl: rabbitctl location
        :param logpath:
        :param path: Path containing rabbitmq'a mnesia na plugins
        :param node_name: RabbitMQ node name
        """
        envvars = {
            "RABBITMQ_LOG_BASE": str(logpath / f"rabbit-server.{port}.log"),
            "RABBITMQ_MNESIA_BASE": str(path / "mnesia"),
            "RABBITMQ_ENABLED_PLUGINS_FILE": str(plugin_path / "plugins"),
            "RABBITMQ_NODE_PORT": str(port),
            "RABBITMQ_DIST_PORT": str(distribution_port),
            # Use the port number in node name, so multiple instances started
            # at different ports will work separately instead of clustering.
            "RABBITMQ_NODENAME": node_name or f"rabbitmq-test-{port}",
        }
        super().__init__(command, host, port, timeout=60, envvars=envvars)
        self.rabbit_ctl = rabbit_ctl

    def rabbitctl_output(self, *args: str) -> str:
        """Query rabbitctl with args.

        :param list args: list of additional args to query
        """
        ctl_command: List[str] = [self.rabbit_ctl]
        ctl_command.extend(args)
        return subprocess.check_output(ctl_command, env=self._popen_kwargs["env"]).decode("utf-8")

    def list_exchanges(self) -> List[str]:
        """Get exchanges defined on given rabbitmq."""
        exchanges: List[str] = []
        output = self.rabbitctl_output("list_exchanges", "name")
        unwanted_exchanges = ["Listing exchanges for vhost / ...", "...done."]

        for exchange in output.split("\n"):
            if exchange and exchange not in unwanted_exchanges:
                exchanges.append(str(exchange))

        return exchanges

    def list_queues(self) -> List[str]:
        """Get queues defined on given rabbitmq."""
        queues: List[str] = []
        output = self.rabbitctl_output("list_queues", "name")

        for queue in output.split("\n"):
            if queue and not self._UNWANTED_QUEUE_PATTERN.search(queue.strip(". ").lower()):
                queues.append(str(queue))

        return queues
