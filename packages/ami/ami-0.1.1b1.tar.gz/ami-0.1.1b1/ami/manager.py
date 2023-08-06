# -*- coding: utf-8 -*-

from __future__ import print_function

import socket
import time
import logging

from .disassembler import PacketDisassembler, GreetingDisassembler
from .assembler import SimpleAssembler
from .event import AmiPublisherSubscriber


logger = logging.getLogger(__name__)


SOCKET_TIMEOUT = 30
SERVE_SLEEP = .1
BUFFER_SIZE = 1024 * 1024
CONNECT_SLEEP = 5

class Manager(object):
    _connection = None
    _host = None
    _port = None
    _secret = None
    _reopen = None

    _assembler = None
    _disassembler = None
    _state_holder = None
    _serve_sleep = 1

    _event = None

    def __init__(self, host, port, user, secret, reopen=True):
        self._host = host
        self._port = port
        self._user = user
        self._secret = secret
        self._reopen = reopen
        self._state_holder = self.StateHolder()
        self._event = AmiPublisherSubscriber()

    def serve_forever(self):
        """ Enter point for blocking listen TCP connection """
        
        self._open()
        self._do_serve()

    def _switch_to_start_state(self):
        self._state_holder.play()
        
        self._assembler = SimpleAssembler()
        self._disassembler = GreetingDisassembler(ongreeting=self._on_greeting)

    def _switch_to_full_state(self):
        self._disassembler = PacketDisassembler(onpacket=self._on_packet)
    
    def _on_greeting(self, greeting):
        logger.info('Succes greeting from {greeting}'.format(greeting=greeting))

        self._switch_to_full_state()
        self._login()

    def _on_packet(self, packet):
        self._event.fire(packet)

    def _do_serve(self):
        while True:
            
            try:
                self._state_holder.check()
            except self.StateHolder.StateHolderPause:
                time.sleep(SERVE_SLEEP)
                continue
            except self.StateHolder.StateHolderStop:
                self._close()
                return
            
            try:
                received = self._connection.recv(BUFFER_SIZE)
            except Exception as error:
                logger.error('Eror when receive from connection - {error}'.format(error=str(error)))
                
                if self._reopen:
                    self._open()

            if received:
                try:
                    self._disassembler(received)
                except Exception as exception:
                    logger.exception('Error when try disassembl')
                    logger.error('Error when try disassembl - {error}'.format(error=str(exception)))

                    if self._reopen:
                        self._open()
                    else:
                        raise exception
            else:
                logger.error('Receive empty data from connection')

                if self._reopen:
                    self._open()
            
            time.sleep(SERVE_SLEEP)

    def _close(self):
        for method, args in [('shutdown', [1]), ('close', [])]:
            try:
                getattr(self._connection, method)(*args)
            except Exception as error:
                logger.error('Error while try close - {error}'.format(error=str(error)))
        
        # for GC
        self._connection = None
        
        logger.info('Close connection on {host}:{port}'.format(host=self._host, port=self._port))


    def _pause_listen(self):
        self._state_holder.pause()

    def _open(self):
        if self._connection is not None:
            self._close()

        self._switch_to_start_state()
        self._connection = self._make_connection()

        logger.info('Open connection on {host}:{port}'.format(host=self._host, port=self._port))

    def _make_connection(self):
        while True:
            try:
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.settimeout(SOCKET_TIMEOUT)
                connection.connect((self._host, self._port))
            except Exception as error:
                logger.error('Error while try connect - {error}'.format(error=str(error)))
                time.sleep(CONNECT_SLEEP)
            else:
                return connection

    def _login(self):
        self.send({
            'Action': 'Login',
            'ActionID': 1,
            'Username': self._user,
            'Secret': self._secret
        })

    def send(self, data):
        try:
            return self._connection.send(self._assembler(data))
        except Exception as error:
            logger.error('Error while try send - {error}'.format(error=str(error)))

    @property
    def event(self):
        return self._event

    class StateHolder(object):
        _state = None

        def stop(self):
            self._state = self.StateHolderStop()

        def pause(self):
            self._state = self.StateHolderPause()
        
        def play(self):
            self._state = self.StateHolderPlay()

        def check(self):
            if not isinstance(self._state, self.StateHolderPlay):
                raise self._state or self.StateHolderNone()

        class StateHolderStop(Exception): pass
        class StateHolderPause(Exception): pass
        class StateHolderPlay(Exception): pass
        class StateHolderNone(Exception): pass
