# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
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

from .command import Command, command_classes


class HandshakeCommand(Command):
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

    def __new__(cls, cmd: dict):
        """
        Create handshake command

        :param cmd: command info
        :return: HandshakeCommand object
        """
        if cmd is None:
            return None
        elif cls is HandshakeCommand:
            if isinstance(cmd, HandshakeCommand):
                # return HandshakeCommand object directly
                return cmd
        # new HandshakeCommand(dict)
        return super().__new__(cls, cmd)

    #
    #   message
    #
    @property
    def message(self) -> str:
        return self['message']

    #
    #   session
    #
    @property
    def session(self) -> str:
        return self.get('session')

    @session.setter
    def session(self, value: str):
        if value is None:
            self.pop('session', None)
        else:
            self['session'] = value

    #
    #   Factories
    #
    @classmethod
    def new(cls, content: dict=None, message: str=None, session: str=None):
        if content is None:
            # create empty content
            content = {}
        # set message string
        if message is not None:
            content['message'] = message
        # set session key
        if session is not None:
            content['session'] = session
        # new HandshakeCommand(dict)
        return super().new(content=content, command=Command.HANDSHAKE)

    @classmethod
    def offer(cls, session: str=None) -> Command:
        """
        Create client-station handshake offer

        :param session: Old session key
        :return: HandshakeCommand object
        """
        return cls.new(message='Hello world!', session=session)

    @classmethod
    def ask(cls, session: str) -> Command:
        """
        Create station-client handshake again with new session

        :param session: New session key
        :return: HandshakeCommand object
        """
        return cls.new(message='DIM?', session=session)

    @classmethod
    def success(cls) -> Command:
        """
        Create station-client handshake success notice

        :return: HandshakeCommand object
        """
        return cls.new(message='DIM!')

    start = offer       # (1. C->S) first handshake, without session
    again = ask         # (2. S->C) ask client to handshake with new session key
    restart = offer     # (3. C->S) handshake with new session key
    accepted = success  # (4. S->C) notice the client that handshake accepted


# register command class
command_classes[Command.HANDSHAKE] = HandshakeCommand
