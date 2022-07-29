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

from abc import ABC, abstractmethod
from typing import Optional, Any, Dict

from dkd import Content


class Command(Content, ABC):
    """
        Command Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            cmd     : "...", // command name
            extra   : info   // command parameters
        }
    """

    # -------- command names begin --------
    META = 'meta'
    DOCUMENT = 'document'
    # -------- command names end --------

    @property
    def cmd(self) -> str:
        """ get command name """
        # return command_name(content=self.dictionary)
        raise NotImplemented

    @classmethod
    def factory(cls, cmd: str):  # -> Optional[CommandFactory]:
        return g_command_factories.get(cmd)

    @classmethod
    def register(cls, cmd: str, factory):
        g_command_factories[cmd] = factory


class CommandFactory:

    @abstractmethod
    def parse_command(self, content: Dict[str, Any]) -> Optional[Command]:
        """
        Parse map object to command

        :param content: command content
        :return: Command
        """
        raise NotImplemented


g_command_factories: Dict[str, CommandFactory] = {}
