from __future__ import print_function

import eventlet
eventlet.monkey_patch()  # noqa (code before rest of imports)

import errno
import inspect
import logging
import logging.config
import os
import re
import signal
import sys
import yaml

from nameko.constants import AMQP_URI_CONFIG_KEY
from nameko.runners import ServiceRunner
from nameko.cli.run import (
    import_service,
    run
)
from nameko_dev.autoreload import main as auto_main


def main(args):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

    if args.config:
        with open(args.config) as fle:
            config = yaml.load(fle)
    else:
        config = {
            AMQP_URI_CONFIG_KEY: args.broker
        }

    if "LOGGING" in config:
        logging.config.dictConfig(config['LOGGING'])
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    services = []
    for path in args.services:
        services.extend(
            import_service(path)
        )

    auto_main(run, [services, config], {'backdoor_port': args.backdoor_port})
