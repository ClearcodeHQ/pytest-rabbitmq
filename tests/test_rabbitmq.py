"""Tests for RabbitMQ fixtures."""
from rabbitpy import Exchange, Queue

from pytest_rabbitmq.factories.client import clear_rabbitmq


def test_rabbitmq(rabbitmq):
    """Check a signle. default rabbitmq."""
    channel = rabbitmq.channel()
    assert channel.state == channel.OPEN


def test_second_rabbitmq(rabbitmq, rabbitmq2):
    """Check whether two rabbitmq are started correctly."""
    print("checking first channel")
    channel = rabbitmq.channel()
    assert channel.state == channel.OPEN

    print("checking second channel")
    channel2 = rabbitmq2.channel()
    assert channel2.state == channel.OPEN


def test_rabbitmq_clear_exchanges(rabbitmq, rabbitmq_proc):
    """Declare exchange, and clear it by clear_rabbitmq."""
    channel = rabbitmq.channel()
    assert channel.state == channel.OPEN

    # list exchanges
    no_exchanges = rabbitmq_proc.list_exchanges()

    # declare exchange and list exchanges afterwards
    exchange = Exchange(channel, "cache-in")
    exchange.declare()
    exchanges = rabbitmq_proc.list_exchanges()

    # make sure it differs
    assert exchanges != no_exchanges
    clear_rabbitmq(rabbitmq_proc, rabbitmq)

    # list_exchanges again and make sure it's empty
    cleared_exchanges = rabbitmq_proc.list_exchanges()
    assert no_exchanges == cleared_exchanges


def test_rabbitmq_clear_queues(rabbitmq, rabbitmq_proc):
    """Declare queue, and clear it by clear_rabbitmq."""
    channel = rabbitmq.channel()
    assert channel.state == channel.OPEN

    # list queues
    no_queues = rabbitmq_proc.list_queues()
    assert not no_queues

    # declare queue, and get new output
    queue = Queue(channel, "fastlane")
    queue.declare()
    queues = rabbitmq_proc.list_queues()
    assert queues

    # make sure it's different and clear it
    assert queues != no_queues
    clear_rabbitmq(rabbitmq_proc, rabbitmq)

    # list_queues again and make sure it's empty
    cleared_queues = rabbitmq_proc.list_queues()
    assert no_queues == cleared_queues


def test_random_port(rabbitmq_rand):
    """Test if rabbit fixture can be started on random port."""
    channel = rabbitmq_rand.channel()
    assert channel.state == channel.OPEN


def test_random_port_node_names(rabbitmq_rand_proc2, rabbitmq_rand_proc3):
    """Test node names for different processes."""
    # pylint:disable=protected-access
    assert (
        rabbitmq_rand_proc2._envvars["RABBITMQ_NODENAME"]
        != rabbitmq_rand_proc3._envvars["RABBITMQ_NODENAME"]
    )
    # pylint:enable=protected-access


def test_plugin_directory(rabbitmq_plugindir):
    """Test node names for different processes."""
    # pylint:disable=protected-access
    assert (
        rabbitmq_plugindir._envvars["RABBITMQ_ENABLED_PLUGINS_FILE"] == "/etc/plugins"
    )
    # pylint:enable=protected-access
