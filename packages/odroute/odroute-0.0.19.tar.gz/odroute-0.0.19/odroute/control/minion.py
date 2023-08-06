# -*- coding: utf-8 -*-
import logging
import zmq
import json

from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream

from .executor import CommandExecutor

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

logger = logging.getLogger(__name__)

class RoutingMinion(CommandExecutor):

    zmq_receive = None
    zmq_send = None

    def __init__(self, master_addr, router):

        super(RoutingMinion, self).__init__(router)

        self.master_addr = master_addr
        self.zmq_connect_to_master()

        self.router = router
        self.router.register_state_change(self.state_changed)


    def __str__(self):
        return '<RoutingMinion: {}>'.format(self.master_addr)


    def zmq_connect_to_master(self):
        """
        establishes bidirectional connection to master controller.
        """

        zmq_ct = zmq.Context()
        addr = urlparse(self.master_addr)

        receiver_addr = '{scheme}://{hostname}:{port}'.format(
            scheme=addr.scheme,
            hostname=addr.hostname,
            port=addr.port
        )
        receiver = zmq_ct.socket(zmq.PULL)
        receiver.connect(receiver_addr)
        self.zmq_receive = receiver
        logger.debug('Connecting minion-receiver to {}'.format(receiver_addr))


        sender_addr = '{scheme}://{hostname}:{port}'.format(
            scheme=addr.scheme,
            hostname=addr.hostname,
            port=addr.port + 1
        )
        sender = zmq_ct.socket(zmq.PUB)
        sender.connect(sender_addr)
        self.zmq_send = sender
        logger.debug('Connecting minion-sender to {}'.format(sender_addr))

        #
        stream_receive = ZMQStream(self.zmq_receive)
        stream_receive.on_recv_stream(self.receive)



    def send(self, frame):
        """
        passing the zmq frame to the output's connection
        """
        self.zmq_send.send(frame, zmq.NOBLOCK)

    def receive(self, stream, msg, *args, **kwargs):
        print(msg[0])



    def state_changed(self, state):

        print('**********************')
        print('RoutingMinion - state changed')
        print('**********************')

        #state = b'dsdf'

        self.send(json.dumps(state))


    def start(self):
        ioloop.IOLoop.instance().start()
        while True:
            pass
