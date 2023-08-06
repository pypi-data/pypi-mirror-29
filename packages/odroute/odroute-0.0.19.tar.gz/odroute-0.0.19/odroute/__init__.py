# -*- coding: utf-8 -*-
import logging
import sys

import click
import click_log

from .router import StreamRouter
from .control.rcserver import RCServer
from .control.minion import RoutingMinion

__version__ = '0.0.19'

logger = logging.getLogger(__name__)


@click.group()
@click_log.init(__name__)
@click.option('--verbose', default=False, is_flag=True)
def cli(verbose):
    if verbose:
        logger.setLevel(logging.DEBUG)


@cli.command()
@click.option('--source', '-s', 'sources', type=int, multiple=True, required=True,
              help='The source ports for incoming connections. Can (and likely will) be given multiple times')
@click.option('--output', '-o', 'outputs', multiple=True, required=True,
              help='Destinations to route to, in the form of: tcp://<hostnam>:<port>. Can be given multiple times')
@click.option('--delay', '-d', default=0.5,
              help='Delay until to fallback to secondary streams')
@click.option('--audio-threshold', '-a', default=-90,
              help='Minimum audio level (range [-90..0] dB) for input to be considered ok. Set to -90 to disable level detection')
@click.option('--telnet', '-t', required=False,
              help='Add telnet interface: <bind addr>:<port> or <port> (if only port is given interface will bind to 127.0.0.1)')
@click.option('--socket', '-S', required=False,
              help='Add unix socket interface: </path/to/socket>')
@click.option('--master', '-m', required=False,
              help='Connect odroute instance to master control-server: tcp://<hostnam>:<port>')
def run(sources, outputs, delay, telnet, socket, audio_threshold, master):

    # logger.info('Source ports: %s' % ', '.join(map(str, sources)))
    # logger.info('Destinations: %s' % ', '.join(outputs))
    # logger.info('Telnet interface: %s' % telnet)
    # logger.info('Socket interface: %s' % socket)

    while True:

        r = StreamRouter(sources, outputs, delay, audio_threshold)

        # adding remote-control interface
        if telnet or socket:
            rc_server = RCServer(router=r)

            if telnet:
                if telnet.isdigit():
                    _address, _port,  = '127.0.0.1', int(telnet)
                else:
                    _address, _port = telnet.split(':')

                logger.info('Binding telnet interface to {}:{}'.format(_address, _port))
                rc_server.bind(address=_address, port=int(_port))

            if socket:
                logger.info('Binding unix socket interface to {}'.format(socket))
                rc_server.add_unix_socket(socket)

            r.register_start_with_ioloop(rc_server)

        # adding client for master control-server setup
        if master:
            #raise NotImplementedError('Sorry - not implemented yet.')

            routing_minion = RoutingMinion(master_addr=master, router=r)

            r.register_start_with_ioloop(routing_minion)


        try:
            r.connect()
            r.start()
        except KeyboardInterrupt:
            logger.info('Ctrl-c received. Stopping router.')
            r.stop()
            sys.exit()

