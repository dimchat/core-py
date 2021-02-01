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

from abc import abstractmethod
from typing import Optional, Union

from dkd import ContentType, BaseContent


class Command(BaseContent):
    """
        Command Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command : "...", // command name
            extra   : info   // command parameters
        }
    """

    # -------- command names begin --------
    META = 'meta'
    DOCUMENT = 'document'

    RECEIPT = 'receipt'
    HANDSHAKE = 'handshake'
    LOGIN = 'login'
    # -------- command names end --------

    def __init__(self, cmd: Optional[dict] = None, content_type: Union[ContentType, int] = 0,
                 command: Optional[str] = None):
        if cmd is None:
            if content_type == 0:
                content_type = ContentType.COMMAND
            super().__init__(content_type=content_type)
        else:
            super().__init__(content=cmd)
        self.__command = command
        if command is not None:
            self['command'] = command

    @property
    def command(self) -> str:
        if self.__command is None:
            self.__command = command_name(cmd=self.dictionary)
        return self.__command

    #
    #  Factory for creating Command
    #
    class Factory:

        @abstractmethod
        def parse_command(self, cmd: dict):  # -> Optional[Command]:
            """
            Parse map object to command

            :param cmd: command info
            :return: Command
            """
            raise NotImplemented

    __factories = {}  # name -> factory

    @classmethod
    def register(cls, command: str, factory: Factory):
        cls.__factories[command] = factory

    @classmethod
    def factory(cls, command: str) -> Factory:
        return cls.__factories.get(command)


"""
    Implements
    ~~~~~~~~~~
"""


def command_name(cmd: dict) -> str:
    return cmd.get('command')
