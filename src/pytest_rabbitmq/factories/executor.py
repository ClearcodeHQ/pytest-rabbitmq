"""RabbitMQ Executor."""

import subprocess

from mirakuru import TCPExecutor


class RabbitMqExecutor(TCPExecutor):
    """RabbitMQ executor to start specific rabbitmq instances."""

    def __init__(self, command, host, port, rabbit_ctl, **kwargs):
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

    def rabbitctl_output(self, *args):
        """
        Query rabbitctl with args.

        :param list args: list of additional args to query
        """
        ctl_command = [self.rabbit_ctl]
        ctl_command.extend(args)
        return subprocess.check_output(
            ctl_command,
            env=self._popen_kwargs['env']
        ).decode('utf-8')

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
