# -*- coding: utf-8 -*-
import logging
import sys
import time
from functools import partial
#from multiprocessing import Queue

import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream

from collections import OrderedDict

from .frame import ZMQFrameDecoder

logger = logging.getLogger(__name__)

ioloop.install()


class StreamInput(object):
    """
    Input instance.
    """

    connected = False

    def __init__(self, zmq_ctx, port, failover_seconds, audio_threshold):
        """
        audio_threshold is in range [-90..0] dB
        """
        self.zmq_ctx = zmq_ctx
        self.port = port
        self.failover_seconds = failover_seconds

        time_now = time.time()
        self._last_beat = time_now - float(failover_seconds)
        self._last_audio_ok = time_now - float(failover_seconds)

        self.stream = self.bind()
        self.frame_decoder = ZMQFrameDecoder()
        self.audio_threshold = audio_threshold

    def __str__(self):
        return '<StreamInput: port {}>'.format(self.port)

    def bind(self):
        """
        bind zmq input port
        """
        logger.debug('Binding socket on port {} - failover delay: {}s'.format(
            self.port,
            self.failover_seconds,
        ))
        s = self.zmq_ctx.socket(zmq.SUB)
        s.bind('tcp://*:{port}'.format(port=self.port))
        s.setsockopt(zmq.SUBSCRIBE, b"")
        self.connected = True
        return ZMQStream(s)

    def stop(self):
        logger.debug('Stopping socket on port {}'.format(self.port))
        # close zmq socket
        self.stream.close()
        self.connected = False

    def tick(self, msg):
        """
        triggered on every `on_recv` - used to track input availability.
        """
        time_now = time.time()
        self._last_beat = time_now

        # always load frame so that the audio levels are visible in the
        # telnet interface
        self.frame_decoder.load_frame(msg)
        if self.audio_threshold != -90:
            audio_left, audio_right = self.frame_decoder.get_audio_levels()
            has_valid_audio = (audio_left is not None) and \
                              (audio_right is not None) and \
                              (audio_left > self.audio_threshold) and \
                              (audio_right > self.audio_threshold)
            if has_valid_audio:
                self._last_audio_ok = time_now
        else:
            # Assume audio is always ok
            self._last_audio_ok = time_now

    @property
    def is_available(self):
        """
        check if the input instance is 'available':
        "last time ticked less than failover duration"
        """
        time_now = time.time()
        has_recently_received_data = self._last_beat > (time_now - float(self.failover_seconds))
        has_valid_audio = self._last_audio_ok > (time_now - float(self.failover_seconds))

        return has_recently_received_data and has_valid_audio

class StreamOutput(object):
    """
    Output instance. Connects to remote socket and relies the zmq frames.
    """

    connected = False

    def __init__(self, zmq_ctx, output):
        self.zmq_ctx = zmq_ctx
        self.output = output
        self.connection = self.connect()

    def __str__(self):
        return '<StreamOutput: {}>'.format(self.output)

    def connect(self):
        logger.debug('Connecting output to {}'.format(self.output))
        c = self.zmq_ctx.socket(zmq.PUB)
        c.connect(self.output)
        self.connected = True
        return c

    def send(self, frame):
        """
        passing the zmq frame to the output's connection
        """
        self.connection.send(frame, zmq.NOBLOCK)


class StreamRouter(object):
    """
    Router instance. Handles input and output connections & routing (priority).
    """
    _inputs = []
    _current_input = None
    _last_input = None
    _forced_input = None
    _outputs = []
    _state = None
    _start_with_ioloop = []
    _state_change_callbacks = []


    def __init__(self, source_ports, destinations, delay, audio_threshold, **options):
        self.failover_seconds = delay
        self.audio_threshold = audio_threshold
        self.zmq_ctx = zmq.Context()
        self.source_ports = source_ports
        self.destinations = destinations

    def get_outputs(self):
        return self._outputs

    def get_inputs(self):
        return self._inputs

    def get_current_inputs(self):
        return self._current_input

    def set_auto_switch(self):
        self._forced_input = None

    def force_input(self, i):
        if i not in self._inputs:
            raise ValueError("Port {} not available".format(i))
        self._forced_input = i

    def connect(self):
        self.bind_inputs()
        self.connect_outputs()

        self.update_state()

    def bind_inputs(self):
        for port in self.source_ports:
            i = StreamInput(self.zmq_ctx, port, self.failover_seconds, self.audio_threshold)
            logger.info('Created input socket on port {}'.format(port))
            self._inputs.append(i)

    def connect_outputs(self):
        for destination in self.destinations:
            o = StreamOutput(self.zmq_ctx, destination)
            logger.info('Connected output to {}'.format(destination))
            self._outputs.append(o)

    def set_current_input(self):
        current_input = None

        # force input
        if self._forced_input:
            filtered_inputs = [i for i in self._inputs if i.port == self._forced_input]
            if filtered_inputs:
                current_input = filtered_inputs[0]

        # Loop through the inputs and return the first available one.
        if not current_input:
            available_inputs = [i for i in self._inputs if i.is_available]
            if available_inputs:
                current_input = available_inputs[0]
            else:
                pass
                # TODO: Raise alarm, no inputs available!


        self._current_input = current_input

        if not current_input == self._last_input:
            logger.info('Switching inputs: {} to {}'.format(self._last_input.port if self._last_input else None, current_input.port))
            self._last_input = current_input
            self.update_state()


    def route(self, stream, msg, input):
        """
        Routes the active input to all outputs
        """

        # Trigger a 'heartbeat' tick on the input.
        input.tick(msg[0])

        self.set_current_input()

        if input == self._current_input:
            for o in self._outputs:
                o.send(msg[0])

    def start(self):
        for i in self._inputs:
            i.stream.on_recv_stream(partial(self.route, input=i))

        for cb in self._start_with_ioloop:
            logger.debug('Starting with ioloop: {}'.format(cb))
            cb.start()

        # Initialise the tornado ioloop
        # http://pyzmq.readthedocs.io/en/latest/eventloop.html#futures-and-coroutines
        io_loop = ioloop.IOLoop.instance()

        pc = ioloop.PeriodicCallback(self.update_state, 2000)
        pc.start()

        io_loop.start()

        while True:
            pass

    def stop(self):
        logger.info('Stopping router')

        for i in self._inputs:
            logger.info('Stopping input on port {}'.format(i.port))
            i.stop()

        sys.exit()


    def register_start_with_ioloop(self, cb):
        if not cb in self._start_with_ioloop:
            self._start_with_ioloop.append(cb)


    def register_state_change(self, cb):
        if not cb in self._state_change_callbacks:
            self._state_change_callbacks.append(cb)


    def update_state(self):
        """
         `StreamRouter._state` holds the router's state information in a dict.
         the `update_state` method collects the current state (inputs, outputs, levels, etc)
        """
        _state = OrderedDict({
            'inputs': [],
            'outputs': [],
            'forced_input': self._forced_input,
        })

        current_input_port = self._current_input.port if self._current_input else None

        for input in self._inputs:
            _state['inputs'].append({
                'port': input.port,
                'available': input.is_available,
                'current': input.port == current_input_port,
            })


        for output in self._outputs:
            _state['outputs'].append({
                'destination': output.output,
                'connected': output.connected,
            })


        if _state != self._state:

            logger.debug('state changed: {}'.format(dict(_state)))

            # send updated state to registered callbacks
            # NOTE: this must be implemented asynchronous
            for cb in self._state_change_callbacks:
                cb(state=_state)

        self._state = _state



