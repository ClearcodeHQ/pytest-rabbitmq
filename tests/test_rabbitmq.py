"""Tests for RabbitMQ fixtures."""

from pika import BlockingConnection

from pytest_rabbitmq.factories.client import clear_rabbitmq
from pytest_rabbitmq.factories.executor import RabbitMqExecutor


def test_rabbitmq(rabbitmq: BlockingConnection) -> None:
    """Check a signle. default rabbitmq."""
    channel = rabbitmq.channel()
    assert channel.is_open


def test_second_rabbitmq(rabbitmq: BlockingConnection, rabbitmq2: BlockingConnection) -> None:
    """Check whether two rabbitmq are started correctly."""
    print("checking first channel")
    channel = rabbitmq.channel()
    assert channel.is_open

    print("checking second channel")
    channel2 = rabbitmq2.channel()
    assert channel2.is_open


def test_rabbitmq_clear_exchanges(
    rabbitmq: BlockingConnection, rabbitmq_proc: RabbitMqExecutor
) -> None:
    """Declare exchange, and clear it by clear_rabbitmq."""
    channel = rabbitmq.channel()
    assert channel.is_open

    # list exchanges
    no_exchanges = rabbitmq_proc.list_exchanges()

    # declare exchange and list exchanges afterwards
    channel.exchange_declare("cache-in")
    exchanges = rabbitmq_proc.list_exchanges()

    # make sure it differs
    assert exchanges != no_exchanges
    clear_rabbitmq(rabbitmq_proc, rabbitmq)

    # list_exchanges again and make sure it's empty
    cleared_exchanges = rabbitmq_proc.list_exchanges()
    assert no_exchanges == cleared_exchanges


def test_rabbitmq_clear_queues(
    rabbitmq: BlockingConnection, rabbitmq_proc: RabbitMqExecutor
) -> None:
    """Declare queue, and clear it by clear_rabbitmq."""
    channel = rabbitmq.channel()
    assert channel.is_open

    # list queues
    no_queues = rabbitmq_proc.list_queues()
    assert not no_queues

    # declare queue, and get new output
    channel.queue_declare("fastlane")
    queues = rabbitmq_proc.list_queues()
    assert queues

    # make sure it's different and clear it
    assert queues != no_queues
    clear_rabbitmq(rabbitmq_proc, rabbitmq)

    # list_queues again and make sure it's empty
    cleared_queues = rabbitmq_proc.list_queues()
    assert no_queues == cleared_queues


def test_random_port(rabbitmq_rand: BlockingConnection) -> None:
    """Test if rabbit fixture can be started on random port."""
    channel = rabbitmq_rand.channel()
    assert channel.is_open


def test_random_port_node_names(
    rabbitmq_rand_proc2: RabbitMqExecutor, rabbitmq_rand_proc3: RabbitMqExecutor
) -> None:
    """Test node names for different processes."""
    # pylint:disable=protected-access
    assert (
        rabbitmq_rand_proc2._envvars["RABBITMQ_NODENAME"]
        != rabbitmq_rand_proc3._envvars["RABBITMQ_NODENAME"]
    )
    # pylint:enable=protected-access


def test_plugin_directory(rabbitmq_plugindir: RabbitMqExecutor) -> None:
    """Test node names for different processes."""
    # pylint:disable=protected-access
    assert rabbitmq_plugindir._envvars["RABBITMQ_ENABLED_PLUGINS_FILE"] == "/etc/plugins"
    # pylint:enable=protected-access
