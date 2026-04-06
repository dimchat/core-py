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
from typing import Optional, Dict

from mkm.types import Converter
from dkd.protocol import Content, Envelope
from dkd.ext import MessageExtensions, shared_message_extensions

from .types import ContentType
from .base import BaseContent


class QuoteContent(Content, ABC):
    """
        Quote Message content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            "type" : i2s(0x37),
            "sn"   : 67890,

            "text"    : "...",  // text message
            "origin"  : {       // original message envelope
                "sender"   : "...",
                "receiver" : "...",

                "type"     : i2s(0x01),
                "sn"       : 12345,
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
        helper = quote_helper()
        origin = helper.purify_for_quote(envelope=envelope, content=content)
        return BaseQuoteContent(text=text, origin=origin)


def quote_helper():
    helper = shared_message_extensions.quote_helper
    assert isinstance(helper, QuoteHelper), 'quote helper error: %s' % helper
    return helper


###############################
#                             #
#   DaoKeDao Implementation   #
#                             #
###############################


class BaseQuoteContent(BaseContent, QuoteContent):

    def __init__(self, content: Dict = None,
                 text: str = None, origin: Dict = None):
        if content is None:
            # 1. new content with text & origin info
            assert not (text is None or origin is None), 'quote error: %s, %s' % (text, origin)
            msg_type = ContentType.QUOTE
            super().__init__(None, msg_type)
            self['text'] = text
            self['origin'] = origin
        else:
            # 2. content info from network
            assert text is None and origin is None, 'quote error: %s, %s' % (text, origin)
            super().__init__(content=content)
        # lazy load
        self.__env: Optional[Envelope] = None

    @property  # Override
    def text(self) -> str:
        return self.get_str(key='text', default='')

    @property  # protected
    def origin(self) -> Optional[Dict]:
        return self.get('origin')

    @property  # Override
    def original_envelope(self) -> Optional[Envelope]:
        env = self.__env
        if env is None:
            # origin: { sender: "...", receiver: "...", time: 0 }
            env = Envelope.parse(envelope=self.origin)
            self.__env = env
        return env

    @property  # Override
    def original_sn(self) -> Optional[int]:
        origin = self.origin
        if origin is not None:
            sn = origin.get('sn')
            return Converter.get_int(value=sn)


# -----------------------------------------------------------------------------
#  Message Extensions
# -----------------------------------------------------------------------------


class QuoteHelper(ABC):

    @abstractmethod
    def purify_for_quote(self, envelope: Envelope, content: Content) -> Dict:
        raise NotImplemented

    @abstractmethod
    def purify_for_receipt(self, envelope: Optional[Envelope], content: Optional[Content]) -> Optional[Dict]:
        raise NotImplemented


class QuotePurifier(QuoteHelper):

    # Override
    def purify_for_quote(self, envelope: Envelope, content: Content) -> Dict:
        source = envelope.sender
        target = content.group
        if target is None:
            target = envelope.receiver
        # build origin info
        return {
            'sender': str(source),
            'receiver': str(target),
            'type': content.type,
            'sn': content.sn,
        }

    # Override
    def purify_for_receipt(self, envelope: Optional[Envelope], content: Optional[Content]) -> Optional[Dict]:
        if envelope is None:
            return None
        origin = envelope.copy_dictionary(deep_copy=False)
        if 'data' in origin:
            origin.pop('data', None)
            origin.pop('key', None)
            origin.pop('keys', None)
            origin.pop('meta', None)
            origin.pop('visa', None)
        if content is not None:
            origin['sn'] = content.sn
        return origin


class _QuoteExt:
    _quote_helper: QuoteHelper = QuotePurifier()

    @property
    def quote_helper(self) -> QuoteHelper:
        return _QuoteExt._quote_helper

    @quote_helper.setter
    def quote_helper(self, helper: QuoteHelper):
        _QuoteExt._quote_helper = helper


MessageExtensions.quote_helper = _QuoteExt.quote_helper
