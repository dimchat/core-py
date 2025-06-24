# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2024 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2024 Albert Moky
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
from typing import Optional, List, Dict, Any

from dkd import Content, Envelope
from dkd import InstantMessage


class QuoteContent(Content, ABC):
    """
        Quote Message content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x37),
            sn   : 456,

            text    : "...",  // text message
            origin  : {       // original message envelope
                sender   : "...",
                receiver : "...",

                type     : 0x01,
                sn       : 123,
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

    #
    #   Factory method
    #

    @classmethod
    def create(cls, text: str, envelope: Envelope, content: Content):
        """
        Create quote content with text & original message info

        :param text:     message text
        :param envelope: original message head
        :param content:  original message body
        :return: ReceiptCommand
        """
        info = cls.purify(envelope=envelope)
        info['type'] = content.type
        info['sn'] = content.sn
        # update: receiver -> group
        group = content.group
        if group is not None:
            info['receiver'] = str(group)
        from ..dkd import BaseQuoteContent
        return BaseQuoteContent(text=text, origin=info)

    @classmethod
    def purify(cls, envelope: Envelope) -> Dict[str, Any]:
        source = envelope.sender
        target = envelope.group
        if target is None:
            target = envelope.receiver
        # build origin info
        info = {
            'sender': str(source),
            'receiver': str(target),
        }
        return info


class CombineContent(Content, ABC):
    """
        Combine Forward message
        ~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0xFF),
            sn   : 456,

            title    : "...",  // chat title
            messages : [...]   // chat history
        }
    """

    @property
    @abstractmethod
    def title(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def messages(self) -> List[InstantMessage]:
        raise NotImplemented

    #
    #   Factory methods
    #
    @classmethod
    def create(cls, title: str, messages: List[InstantMessage]):
        from ..dkd import CombineForwardContent
        return CombineForwardContent(title=title, messages=messages)
