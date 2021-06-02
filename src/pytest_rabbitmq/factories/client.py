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
"""RabbitMQ client fixture factory."""
import logging

import pytest

from rabbitpy import Exchange, Queue, Connection
from rabbitpy.exceptions import ChannelClosedException

logger = logging.getLogger("pytest-rabbitmq")


def clear_rabbitmq(process, rabbitmq_connection):
    """
    Clear queues and exchanges from given rabbitmq process.

    :param RabbitMqExecutor process: rabbitmq process
    :param rabbitpy.Connection rabbitmq_connection: connection to rabbitmq

    """
    channel = rabbitmq_connection.channel()

    for exchange in process.list_exchanges():
        if exchange.startswith("amq."):
            # ----------------------------------------------------------------
            # From rabbit docs:
            # https://www.rabbitmq.com/amqp-0-9-1-reference.html
            # ----------------------------------------------------------------
            # Exchange names starting with "amq." are reserved for pre-declared
            # and standardised exchanges. The client MAY declare an exchange
            # starting with "amq." if the passive option is set, or the
            # exchange already exists. Error code: access-refused
            # ----------------------------------------------------------------
            continue
        ex = Exchange(channel, exchange)
        ex.delete()

    for queue_name in process.list_queues():
        if queue_name.startswith("amq."):
            # ----------------------------------------------------------------
            # From rabbit docs:
            # https://www.rabbitmq.com/amqp-0-9-1-reference.html
            # ----------------------------------------------------------------
            # Queue names starting with "amq." are reserved for pre-declared
            # and standardised queues. The client MAY declare a queue starting
            # with "amq." if the passive option is set, or the queue already
            # exists. Error code: access-refused
            # ----------------------------------------------------------------
            continue
        queue = Queue(channel, queue_name)
        queue.delete()


def rabbitmq(process_fixture_name, teardown=clear_rabbitmq):
    """
    Client fixture factory for RabbitMQ.

    :param str process_fixture_name: name of RabbitMQ process variable
        returned by rabbitmq_proc
    :param callable teardown: custom callable that clears rabbitmq

    .. note::

        calls to rabbitmqctl might be as slow or even slower
        as restarting process. To speed up, provide Your own teardown function,
        to remove queues and exchanges of your choosing, without querying
        rabbitmqctl underneath.

    :returns RabbitMQ connection
    """

    @pytest.fixture
    def rabbitmq_factory(request):
        """
        Client fixture for RabbitMQ.

        #. Get module and config.
        #. Connect to RabbitMQ using the parameters from config.

        :param TCPExecutor rabbitmq_proc: tcp executor
        :param FixtureRequest request: fixture request object
        :rtype: rabbitpy.adapters.blocking_connection.BlockingConnection
        :returns: instance of :class:`BlockingConnection`
        """
        # load required process fixture
        process = request.getfixturevalue(process_fixture_name)

        connection = Connection(f"amqp://guest:guest@{process.host}:{process.port}/%2F")

        yield connection
        teardown(process, connection)
        try:
            connection.close()
        except ChannelClosedException as e:
            # at this stage this exception occurs when connection is being closed
            logger.warning(f"ChannelClosedException occured while closing connection {e}")

    return rabbitmq_factory
