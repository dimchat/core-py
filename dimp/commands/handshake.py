# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

"""
    Handshake Command Protocol
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    1. (C-S) handshake start
    2. (S-C) handshake again with new session
    3. (C-S) handshake start with new session
    4. (S-C) handshake success
"""

from dkd.contents import serial_number

from dkd import MessageType, CommandContent


class HandshakeCommand(CommandContent):
    """
        Handshake Command
        ~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command : "handshake",    // command name
            message : "Hello world!", // "DIM?", "DIM!"
            session : "{SESSION_ID}", // session key
        }
    """

    #
    #   message
    #
    @property
    def message(self) -> str:
        return self.get('message')

    @message.setter
    def message(self, value: str):
        if value:
            self['message'] = value
        else:
            self.pop('message')

    #
    #   session
    #
    @property
    def session(self) -> str:
        return self.get('session')

    @session.setter
    def session(self, value: str):
        if value:
            self['session'] = value
        else:
            self.pop('session')

    #
    #   Factories
    #
    @classmethod
    def handshake(cls, message: str='Hello world!', session: str=None) -> CommandContent:
        content = {
            'type': MessageType.Command,
            'sn': serial_number(),
            'command': 'handshake',
            'message': message,
        }
        if session:
            content['session'] = session
        return HandshakeCommand(content)

    @classmethod
    def offer(cls, session: str =None) -> CommandContent:
        """
        Create client-station handshake offer

        :param session: Old session key
        :return: HandshakeCommand object
        """
        return cls.handshake(session=session)

    @classmethod
    def ask(cls, session: str) -> CommandContent:
        """
        Create station-client handshake again with new session

        :param session: New session key
        :return: HandshakeCommand object
        """
        return cls.handshake(message='DIM?', session=session)

    @classmethod
    def success(cls) -> CommandContent:
        """
        Create station-client handshake success notice

        :return: HandshakeCommand object
        """
        return cls.handshake(message='DIM!')

    start = offer       # (1. C->S) first handshake, without session
    again = ask         # (2. S->C) ask client to handshake with new session key
    restart = offer     # (3. C->S) handshake with new session key
    accepted = success  # (4. S->C) notice the client that handshake accepted
