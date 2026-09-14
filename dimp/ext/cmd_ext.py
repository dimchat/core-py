# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
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
from typing import Optional

from mkm.types import StrMap

from dkd.protocol import Envelope
from dkd.protocol import Content
from dkd.ext import MessageExtensions, shared_message_extensions

from ..protocol import Command


class CommandHandler(ABC):
    """ General Command Helper """

    @abstractmethod
    def get_cmd(self, content: StrMap, default: str = None) -> Optional[str]:
        """
        Get command name from content

        :param content: command content
        :param default: default command name
        :return: command name
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_cmd()'
        )

    @abstractmethod
    def create_receipt(self, text: str, envelope: Envelope, content: Optional[Content]) -> Command:
        """
        Create receipt command

        :param text: receipt text
        :param envelope: original message envelope
        :param content:  original message content
        :return: ReliableMessage
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_receipt()'
        )


class GeneralCommandExtension:

    @property
    def command_handler(self) -> Optional[CommandHandler]:
        """ Get command helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.command_handler getter'
        )

    @command_handler.setter
    def command_handler(self, helper: CommandHandler):
        """ Set command helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.command_handler setter'
        )


shared_message_extensions.command_handler: Optional[CommandHandler] = None


def message_extensions() -> MessageExtensions:
    return shared_message_extensions


def command_handler() -> CommandHandler:
    ext = message_extensions()
    return ext.command_handler
