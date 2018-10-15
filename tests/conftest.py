"""Tests main conftest file."""
import sys
import warnings

from pytest_rabbitmq import factories

if not sys.version_info >= (3, 5):
    warnings.simplefilter("error", category=DeprecationWarning)


# pylint:disable=invalid-name
rabbitmq_proc2 = factories.rabbitmq_proc(port=5674, node='test2')
rabbitmq2 = factories.rabbitmq('rabbitmq_proc2')
rabbitmq_rand_proc = factories.rabbitmq_proc(port=None, node='test3')
rabbitmq_rand = factories.rabbitmq('rabbitmq_rand_proc')
rabbitmq_rand_proc2 = factories.rabbitmq_proc(port=None)
rabbitmq_rand_proc3 = factories.rabbitmq_proc(port=None)
# pylint:enable=invalid-name
