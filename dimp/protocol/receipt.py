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
from typing import Optional, Dict

from dkd import Envelope, InstantMessage, ReliableMessage

from .commands import Command


class ReceiptCommand(Command):
    """
        Receipt Command
        ~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
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

    @property  # protected
    @abstractmethod
    def origin(self) -> Optional[Dict]:
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
    def create(cls, text: str, msg: ReliableMessage = None):
        """
        Create receipt with text message and origin message envelope

        :param text: message text
        :param msg:  origin message
        :return: ReceiptCommand
        """
        if msg is None:
            assert text is not None, 'cannot create empty receipt command'
            envelope = None
        else:
            info = msg.copy_dictionary(deep_copy=False)
            info.pop('data', None)
            info.pop('key', None)
            info.pop('keys', None)
            info.pop('meta', None)
            info.pop('visa', None)
            assert 'sender' in info, 'message envelope error: %s' % info
            envelope = Envelope.parse(envelope=info)
        # create base receipt command with text & original envelope
        from ..dkd import BaseReceiptCommand
        return BaseReceiptCommand.from_text(text=text, envelope=envelope)


# noinspection PyAbstractClass
class ReceiptCommandMixIn(ReceiptCommand):

    def match_message(self, msg: InstantMessage) -> bool:
        if self.origin is None:
            # receipt without original message info
            return False
        # check signature
        sig1 = self.original_signature
        if sig1 is not None:
            # if contains signature, check it
            sig2 = msg.get_str(key='signature')
            if sig2 is not None:
                return match_signatures(sig1, sig2)
        # check envelope
        env1 = self.original_envelope
        if env1 is not None:
            # if contains envelope, check it
            if not match_envelopes(env1, msg.envelope):
                return False
        # check serial number
        # (only the original message's receiver can know this number)
        return self.original_sn == msg.content.sn


def match_signatures(sig1: str, sig2: str) -> bool:
    if len(sig1) > 8:
        sig1 = sig1[-8:]
    if len(sig2) > 8:
        sig2 = sig2[-8:]
    return sig1 == sig2


def match_envelopes(env1: Envelope, env2: Envelope) -> bool:
    if env1.sender != env2.sender:
        return False
    to1 = env1.group
    if to1 is None:
        to1 = env1.receiver
    to2 = env2.group
    if to2 is None:
        to2 = env2.receiver
    return to1 == to2
