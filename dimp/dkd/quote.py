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

from typing import Optional, Any, Dict, List

from mkm.types import Converter
from dkd import Envelope, InstantMessage

from ..protocol import ContentType
from ..protocol import QuoteContent
from ..protocol import CombineContent

from .contents import BaseContent


class BaseQuoteContent(BaseContent, QuoteContent):
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

    def __init__(self, content: Dict[str, Any] = None,
                 text: str = None, origin: Dict[str, Any] = None):
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
        self.__env = None

    @property  # Override
    def text(self) -> str:
        return self.get_str(key='text', default='')

    @property  # protected
    def origin(self) -> Optional[Dict]:
        return self.get('origin')

    @property  # Override
    def original_envelope(self) -> Optional[Envelope]:
        if self.__env is None:
            # origin: { sender: "...", receiver: "...", time: 0 }
            self.__env = Envelope.parse(envelope=self.origin)
        return self.__env

    @property  # Override
    def original_sn(self) -> Optional[int]:
        origin = self.origin
        if origin is not None:
            sn = origin.get('sn')
            return Converter.get_int(value=sn, default=None)


class CombineForwardContent(BaseContent, CombineContent):
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

    def __init__(self, content: Dict[str, Any] = None,
                 title: str = None, messages: List[InstantMessage] = None):
        if content is None:
            # 1. new content with message(s)
            assert not (title is None or messages is None), 'params error: %s, %s' % (title, messages)
            msg_type = ContentType.COMBINE_FORWARD
            super().__init__(None, msg_type)
            self['messages'] = InstantMessage.revert(messages=messages)
        else:
            # 2. content info from network
            assert title is None and messages is None, 'params error: %s, %s' % (title, messages)
            super().__init__(content)
        # lazy
        self.__messages = messages

    @property  # Override
    def title(self) -> str:
        return self.get_str(key='title', default='')

    @property  # Override
    def messages(self) -> List[InstantMessage]:
        if self.__messages is None:
            array = self.get('messages')
            if array is not None:
                self.__messages = InstantMessage.convert(array=array)
        return self.__messages
