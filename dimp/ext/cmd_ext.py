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


# -----------------------------------------------------------------------------
#  General Command Helpers
# -----------------------------------------------------------------------------


class CommandHandler(ABC):
    """A helper interface for extracting command names from structured command content.

    This interface provides a standardized way to retrieve command identifiers
    from command payloads (typically Map-based), with support for default values.

    Corresponds to the Java interface ``chat.dim.ext.CommandHandler``.
    """

    #
    #  CMD - Command, Method, Declaration
    #

    @abstractmethod
    def get_cmd(self, content: StrMap, default: str = None) -> Optional[str]:
        """Retrieves the command name from a structured command content Map.

        Looks up the command name key (e.g., "command") in the ``content`` Map
        and returns its value. If the key is not found or the value is null,
        returns the ``default`` (if provided).

        :param content: structured command payload (Map) to extract the command name from
        :param default: optional fallback value if the command name is not found
        :return: extracted command name, or the ``default``, or None if neither exists
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_cmd()'
        )

    #
    #  Receipt
    #

    @abstractmethod
    def create_receipt(self, text: str, envelope: Envelope, content: Optional[Content]) -> Command:
        """Create ReceiptCommand with original envelope info.

        Extracts and cleans up metadata from the original message envelope/content
        to form the "origin" field in receipt commands (removes sensitive/redundant fields).

        :param text: message
        :param envelope: original message envelope
        :param content: original instant message content (optional)
        :return: ``Command`` receipt
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_receipt()'
        )


class GeneralCommandExtension:
    """General Extensions.

    (Command Handler extension)
    """

    @property
    def command_handler(self) -> Optional[CommandHandler]:
        """Get the general command handler.

        Corresponds to the Java static field ``SharedCommandExtensions.handler``.
        (Named ``command_handler`` to avoid conflict with the ``handler`` getter
        of ``MessageHandler`` defined in the dkd package.)
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.command_handler getter'
        )

    @command_handler.setter
    def command_handler(self, helper: CommandHandler):
        """Set the general command handler.

        Corresponds to the Java static field ``SharedCommandExtensions.handler``.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.command_handler setter'
        )


shared_message_extensions.command_handler: Optional[CommandHandler] = None


def message_extensions() -> MessageExtensions:
    return shared_message_extensions


def command_handler() -> CommandHandler:
    ext = message_extensions()
    return ext.command_handler
