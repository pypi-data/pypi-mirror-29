# Set IP on default network interface
#
# Copyright (c) 2018 Johnny Wezel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, absolute_import
import argparse
import logging
import itertools
import subprocess
import signal
from datetime import datetime
from subprocess import check_output
import logging.config
import time
import sys
import re

from jw.util.os import SetMinimalEnvironment
from jw.util.python3hell import SetDefaultEncoding, Open
from builtins import object
from pkg_resources import get_distribution, iter_entry_points
import os

SetDefaultEncoding()
SetMinimalEnvironment(override=('HOME',))

LOG_LEVELS = logging._nameToLevel if sys.version_info[:2] > (3, 3) else logging._levelNames
DEFAULT_LOG_FILE = '/var/log/ip-service'
DEFAULT_SSH_PORT = 22
DEFAULT_GENERATIONS = 30
# Program version info
__version__ = get_distribution('jw.ip-service').version
VERSION_INFO = """ip-service %s
Copyright (c) 2014-2015 Johnny Wezel
License: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.""" % __version__

ROUTE_LIST_PARSER_RE = re.compile(
    r'default via (?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?) dev (\w+)'
)
IP_PARSER_RE = re.compile(
    r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(/\d{1,3})?$'
)

# Python3 hell
if sys.version_info.major < 3:
    def str2bytes(s):
        return s
else:
    def str2bytes(s):
        return bytes(s, 'utf-8', 'replace')

class Version(argparse.Action):
    """
    Action: Display version
    """

    def __call__(self, *args, **kw):
        """
        Display version
        """
        print(VERSION_INFO)
        sys.exit(0)

def ReportSignal(signal, frame):
    """
    Report a signal
    """
    logging.info('Received signal %d', signal)

def IpWithOptionalNetwork(s):
    """
    Check wether string is an IP with optional slash and network bitmask size
    """
    assert IP_PARSER_RE.match(s), '%s is not a valid IP' % s
    return s

def DefaultInterface():
    """
    Returns the default network interface
    :return: default network interface
    :rtype: str

    Runs the command `ip route list` and parses the default network interface from the output
    """
    routeOutput = check_output(('ip', 'route', 'list')).decode('utf-8')
    match = ROUTE_LIST_PARSER_RE.match(routeOutput)
    assert match, "Could not parse output of ip route list: %s" % routeOutput
    if match:
        return match.group(1)

def Main():
    """
    Main program
    :return: 0 if no errors occurred
    :rtype: int
    """
    logconfig = {
        'logging': {
            'version': 1,
            'formatters': {
                'default': {
                    'format': '%(asctime)s:%(name)-24s:%(levelname)s: %(message)s'
                }
            },
            'handlers': {
                'default': {
                    'class': 'logging.FileHandler',
                    'formatter': 'default',
                    'filename': DEFAULT_LOG_FILE,
                }
            },
            'loggers': {
                'backup': {
                    'handlers': ['default'],
                    'level': 'INFO'
                }
            }
        }
    }
    # Setup argument parser
    argp = argparse.ArgumentParser(description='Set IP on network interface')
    argp.add_argument(
        '--version',
        '-V',
        action=Version,
        nargs=0,
        help='display version and license information'
    )
    argp.add_argument(
        '--log-level',
        '-L',
        action='store',
        default='INFO',
        choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
        help='set log level (default INFO)'
    )
    argp.add_argument(
        '--log-file',
        '-l',
        action='store',
        default=DEFAULT_LOG_FILE,
        help='set log file (default: %s)' % DEFAULT_LOG_FILE
    )
    argp.add_argument(
        '--interface',
        '-i',
        action='store',
        default=DefaultInterface(),
        help='set interface (default: %s)' % DefaultInterface()
    )
    argp.add_argument(
        '--ip',
        '-a',
        type=IpWithOptionalNetwork,
        action='append',
        required=True,
        help='IP to set'
    )
    argp.add_argument(
        'command',
        action='store',
        nargs='*',
        help='command to run (optional)'
    )
    # Parse arguments
    args = argp.parse_args()
    # Load configurationHide
    logging.basicConfig(
        stream=Open(args.log_file, mode='a', buffering=1),
        level=LOG_LEVELS[args.log_level],
        format='%(asctime)s %(levelname)-8s %(name)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.debug('ip-service version %s started' % __version__)
    logging.debug('Args: %s', args)
    signal.signal(signal.SIGINT, ReportSignal)
    signal.signal(signal.SIGTERM, ReportSignal)
    signal.signal(signal.SIGUSR1, ReportSignal)
    signal.signal(signal.SIGUSR2, ReportSignal)
    signal.signal(signal.SIGHUP, ReportSignal)
    for ip in args.ip:
        logging.info('Setting IP %s for network interface %s', ip, args.interface)
        subprocess.check_call(('ip', 'address', 'add', ip, 'dev', args.interface))
    if args.command:
        logging.debug('Running %s', ' '.join(args.command))
        status = subprocess.call(args.command)
        if status:
            logging.warning('Command returned %d', status)
    else:
        logging.debug('Waiting forever')
        from threading import  Event
        signal.pause()
    for ip in args.ip:
        logging.info('Removing IP %s from network interface %s', ip, args.interface)
        subprocess.check_call(('ip', 'address', 'del', ip, 'dev', args.interface))
    logging.debug('Terminating')
    return 0

if __name__ == '__main__':
    sys.exit(Main())
