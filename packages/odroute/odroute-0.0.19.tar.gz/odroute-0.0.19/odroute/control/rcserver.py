# -*- coding: utf-8 -*-
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.netutil import bind_unix_socket
from tornado.tcpserver import TCPServer

from .executor import CommandExecutor

RC_PROMPT_PREFIX = b'> '

class RCServer(TCPServer, CommandExecutor):
    """
    exposes a control interface via telnet and/or unix-socket
    """
    router = None

    def __init__(self, router):
        self.router = router
        super(RCServer, self).__init__()


    def __str__(self):
        return '<RCServer>'

    def add_unix_socket(self, socket):
        """
        helper method to add file-based socket by path.
        so we can avoid that `bind_unix_socket` has to be imported at the place the
        `RCServer` is initialised.
        """
        self.add_socket(bind_unix_socket(socket))

    @gen.coroutine
    def handle_stream(self, stream, address):
        """
        handle telnet connection
        http://www.tornadoweb.org/en/stable/gen.html#tornado-gen-simplify-asynchronous-code
        """
        #stream.write(RC_PROMPT_PREFIX)
        while True:
            try:
                command = yield stream.read_until(b'\n')
                try:
                    result = self.handle_command(command.decode().strip())
                except TypeError as e:
                    result = 'Error: {}'.format(e)
                yield stream.write(result.encode() + RC_PROMPT_PREFIX)
            except StreamClosedError:
                break
