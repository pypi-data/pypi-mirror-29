"""Amazon Dash.
"""

import argparse
import logging

import sys

from amazon_dash.config import check_config
from amazon_dash.exceptions import AmazonDashException
from amazon_dash.listener import Listener, test_device

CONFIG_FILE = 'amazon-dash.yml'


def create_logger(name, level=logging.INFO):
    """Create a Logger and set handler and formatter

    :param name: logger name
    :param level: logging level
    :return: None
    """
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)-7s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


def set_default_subparser(self, name, args=None):
    """default subparser selection. Call after setup, just before parse_args()
    name: is the name of the subparser to call by default
    args: if set is the argument list handed to parse_args()
    , tested with 2.7, 3.2, 3.3, 3.4
    it works with 2.6 assuming argparse is installed

    :param str name: default command
    :param list args: defaults args for default command
    """
    subparser_found = False
    for arg in sys.argv[1:]:
        if arg in ['-h', '--help']:  # global help if no subparser
            break
    else:
        for x in self._subparsers._actions:
            if not isinstance(x, argparse._SubParsersAction):
                continue
            for sp_name in x._name_parser_map.keys():
                if sp_name in sys.argv[1:]:
                    subparser_found = True
        if not subparser_found:
            # insert default in first position, this implies no
            # global options without a sub_parsers specified
            if args is None:
                sys.argv.insert(1, name)
            else:
                args.insert(0, name)

argparse.ArgumentParser.set_default_subparser = set_default_subparser


def execute_args(args):
    """Execute args.which command

    :param args: argparse args
    :return: None
    """
    if not getattr(args, 'which', None) or args.which == 'run':
        Listener(args.config).run(root_allowed=args.root_allowed)
    elif args.which == 'check-config':
        check_config(args.config)
    elif args.which == 'test-device':
        test_device(args.device, args.config, args.root_allowed)
    elif args.which == 'discovery':
        from amazon_dash.discovery import discover
        discover()


def execute_from_command_line(argv=None):
    """A simple method that runs a ManagementUtility.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default=CONFIG_FILE, help='Path to config file.')

    parser.add_argument('--warning', help='set logging to warning', action='store_const', dest='loglevel',
                        const=logging.WARNING, default=logging.INFO)
    parser.add_argument('--quiet', help='set logging to ERROR', action='store_const', dest='loglevel',
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument('--debug', help='set logging to DEBUG',
                        action='store_const', dest='loglevel',
                        const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('--verbose', help='set logging to COMM',
                        action='store_const', dest='loglevel',
                        const=5, default=logging.INFO)
    parser.sub = parser.add_subparsers()

    parse_service = parser.sub.add_parser('discovery', help='Discover Amazon Dash device on network.')
    parse_service.set_defaults(which='discovery')

    parse_service = parser.sub.add_parser('check-config', help='Validate the configuration file.')
    parse_service.set_defaults(which='check-config')

    parse_service = parser.sub.add_parser('test-device', help='Test a configured device without press button.')
    parse_service.set_defaults(which='test-device')
    parse_service.add_argument('device', help='MAC address')
    parse_service.add_argument('--root-allowed', action='store_true')

    parse_oneshot = parser.sub.add_parser('run', help='Run server')
    parse_oneshot.set_defaults(which='run')
    parse_oneshot.add_argument('--root-allowed', action='store_true')


    parser.set_default_subparser('run')
    args = parser.parse_args(argv[1:])

    create_logger('amazon-dash', args.loglevel)
    try:
        execute_args(args)
    except AmazonDashException as e:
        sys.stderr.write('[Error] Amazon Dash Exception:\n{}\n'.format(e))
