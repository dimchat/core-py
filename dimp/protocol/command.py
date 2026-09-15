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
from typing import Any, Optional

from mkm.types import StrMap

from dkd.protocol import Content
from dkd.ext import MessageExtensions, shared_message_extensions


class Command(Content, ABC):
    """
        Command message content interface.

        Base interface for all command-type messages, which are used to send
        operational instructions with parameters between entities.

        JSON format:
        ```json
        {
          "type"  : i2s(0x88),
          "sn"    : 12345,

          "time"  : 123.45,
          "group" : "group@zzz",

          "command" : "...",  // Unique command name/identifier
          "extra"   : info    // Optional command parameters (dynamic structure)
        }
        ```
    """

    #
    #  Command name
    #

    @property
    @abstractmethod
    def cmd(self) -> str:
        """
        Get command name

        Returns the command/method/declaration name.

        :return: command/method/declaration name
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.cmd getter'
        )

    #
    #   Factory method
    #

    @classmethod
    def parse(cls, content: Any):  # -> Optional[Command]:
        """
        Parse any object to command
        """
        helper = command_helper()
        return helper.parse_command(content=content)

    @classmethod
    def get_factory(cls, cmd: str):  # -> Optional[CommandFactory]:
        """
        Get command factory for name (cmd)
        """
        helper = command_helper()
        return helper.get_command_factory(cmd=cmd)

    @classmethod
    def set_factory(cls, cmd: str, factory):
        """
        Set command factory for name (cmd)
        """
        helper = command_helper()
        helper.set_command_factory(cmd=cmd, factory=factory)


class CommandFactory(ABC):
    """
    Factory interface for parsing command messages from map objects.

    Provides a standardized way to convert raw map data (from JSON) into
    strongly-typed `Command` instances.
    """

    @abstractmethod
    def parse_command(self, content: StrMap) -> Optional[Command]:
        """
        Parses a map object (from JSON) into a `Command` instance.

        :param content: raw map data containing command information
        :return: `Command` instance if parsing succeeds, None otherwise
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_command()'
        )


# -----------------------------------------------------------------------------
#  Message Extensions
# -----------------------------------------------------------------------------


class CommandHelper(ABC):
    """
    General Helper

    Helper interface for registering and using command factories
    to parse command messages from raw content.
    """

    @abstractmethod
    def set_command_factory(self, cmd: str, factory: CommandFactory):
        """
        Set command factory for name (cmd)

        :param cmd:     command name
        :param factory: command factory
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.set_command_factory()'
        )

    @abstractmethod
    def get_command_factory(self, cmd: str) -> Optional[CommandFactory]:
        """
        Get command factory for name (cmd)

        :param cmd: command name
        :return: CommandFactory
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_command_factory()'
        )

    @abstractmethod
    def parse_command(self, content: Any) -> Optional[Command]:
        """
        Parse any object to command

        :param content: command info
        :return: Command object
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_command()'
        )


class CommandExtension:
    """ Command Extension """

    @property
    def command_helper(self) -> Optional[CommandHelper]:
        """ Get command helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.command_helper getter'
        )

    @command_helper.setter
    def command_helper(self, helper: CommandHelper):
        """ Set command helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.command_helper setter'
        )


shared_message_extensions.command_helper: Optional[CommandHelper] = None


def message_extensions() -> MessageExtensions:
    return shared_message_extensions


def command_helper() -> CommandHelper:
    ext = message_extensions()
    return ext.command_helper
