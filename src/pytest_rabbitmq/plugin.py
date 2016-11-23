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
from path import Path

from pytest_rabbitmq import factories


ROOT_DIR = Path(__file__).parent.parent.abspath()
CONF_DIR = ROOT_DIR / 'pytest_rabbitmq' / 'conf'


def pytest_addoption(parser):
    """Confioguration option."""
    parser.addoption(
        '--rabbitmq-logsdir',
        action='store',
        default='/tmp',
        metavar='path',
        dest='rabbitmq_logsdir',
    )


rabbitmq_proc = factories.rabbitmq_proc()
rabbitmq = factories.rabbitmq('rabbitmq_proc')
