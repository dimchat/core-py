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
    Receipt Protocol
    ~~~~~~~~~~~~~~~~

    As receipt returned to sender to proofing the message's received
"""

from abc import abstractmethod
from typing import Optional, Dict, Any

from dkd import Envelope, Content

from .commands import Command


class ReceiptCommand(Command):
    """
        Receipt Command
        ~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x88),
            sn   : 456,

            command : "receipt",
            text    : "...",  // text message
            origin  : {       // original message envelope
                sender    : "...",
                receiver  : "...",
                time      : 0,

                sn        : 123,
                signature : "..."
            }
        }
    """

    @property
    @abstractmethod
    def text(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def original_envelope(self) -> Optional[Envelope]:
        raise NotImplemented

    @property
    @abstractmethod
    def original_sn(self) -> Optional[int]:
        raise NotImplemented

    @property
    @abstractmethod
    def original_signature(self) -> Optional[str]:
        raise NotImplemented

    #
    #   Factory method
    #

    @classmethod
    def create(cls, text: str, envelope: Envelope = None, content: Content = None):
        """
        Create base receipt command with text & original message info

        :param text:     message text
        :param envelope: original message head
        :param content:  original message body
        :return: ReceiptCommand
        """
        # get original info
        if envelope is None:
            info = None
        elif content is None:
            info = cls.purify(envelope=envelope)
        else:
            info = cls.purify(envelope=envelope)
            info['sn'] = content.sn
        # create receipt with text & original info
        from ..dkd import BaseReceiptCommand
        command = BaseReceiptCommand(text=text, origin=info)
        # check group in original content
        if content is not None:
            group = content.group
            if group is not None:
                command.group = group
        # OK
        return command

    @classmethod
    def purify(cls, envelope: Envelope) -> Dict[str, Any]:
        info = envelope.copy_dictionary(deep_copy=False)
        if 'data' in info:
            info.pop('data', None)
            info.pop('key', None)
            info.pop('keys', None)
            info.pop('meta', None)
            info.pop('visa', None)
        return info
