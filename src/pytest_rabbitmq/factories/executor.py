"""RabbitMQ Executor."""
import re
import subprocess

from mirakuru import TCPExecutor


class RabbitMqExecutor(TCPExecutor):
    """RabbitMQ executor to start specific rabbitmq instances."""

    _UNWANTED_QUEUE_PATTERN = re.compile("(done|timeout:|listing queues)")

    def __init__(
        self,
        command,
        host,
        port,
        rabbit_ctl,
        logpath,
        path,
        plugin_path,
        node_name=None,
        **kwargs,
    ):  # pylint:disable=too-many-arguments
        """
        Initialize RabbitMQ executor.

        :param str command: rabbitmq-server location
        :param str host: host where rabbitmq will be accessible
        :param int port: port under which rabbitmq runs
        :param str rabbit_ctl: rabbitctl location
        :param str logpath:
        :param str path: Path containing rabbitmq'a mnesia na plugins
        :param str node_name: RabbitMQ node name
        :param kwargs: see TCPExecutor for description
        """
        envvars = {
            "RABBITMQ_LOG_BASE": logpath + f"/rabbit-server.{port}.log",
            "RABBITMQ_MNESIA_BASE": path + "mnesia",
            "RABBITMQ_ENABLED_PLUGINS_FILE": plugin_path + "/plugins",
            "RABBITMQ_NODE_PORT": str(port),
            # Use the port number in node name, so multiple instances started
            # at different ports will work separately instead of clustering.
            "RABBITMQ_NODENAME": node_name or f"rabbitmq-test-{port}",
        }
        super().__init__(command, host, port, timeout=60, envvars=envvars, **kwargs)
        self.rabbit_ctl = rabbit_ctl

    def rabbitctl_output(self, *args):
        """
        Query rabbitctl with args.

        :param list args: list of additional args to query
        """
        ctl_command = [self.rabbit_ctl]
        ctl_command.extend(args)
        return subprocess.check_output(ctl_command, env=self._popen_kwargs["env"]).decode("utf-8")

    def list_exchanges(self):
        """Get exchanges defined on given rabbitmq."""
        exchanges = []
        output = self.rabbitctl_output("list_exchanges", "name")
        unwanted_exchanges = ["Listing exchanges ...", "...done."]

        for exchange in output.split("\n"):
            if exchange and exchange not in unwanted_exchanges:
                exchanges.append(str(exchange))

        return exchanges

    def list_queues(self):
        """Get queues defined on given rabbitmq."""
        queues = []
        output = self.rabbitctl_output("list_queues", "name")

        for queue in output.split("\n"):
            if queue and not self._UNWANTED_QUEUE_PATTERN.search(queue.strip(". ").lower()):
                queues.append(str(queue))

        return queues
