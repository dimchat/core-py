# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2021 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2021 Albert Moky
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

from typing import Optional, Any, Dict

from mkm.types import DateTime
from mkm import ID

from dkd import Content
from dkd import Envelope
from dkd import InstantMessage

from .base import BaseMessage


"""
    Instant Message
    ~~~~~~~~~~~~~~~

    data format: {
        //-- envelope
        sender   : "moki@xxx",
        receiver : "hulk@yyy",
        time     : 123,
        //-- content
        content  : {...}
    }
"""


class PlainMessage(BaseMessage, InstantMessage):

    def __init__(self, msg: Dict[str, Any] = None,
                 head: Envelope = None, body: Content = None):
        if msg is None:
            # 1. new instant message with envelope & content
            assert head is not None and body is not None, 'instant message error: %s, %s' % (head, body)
            super().__init__(None, head)
            self['content'] = body.dictionary
        else:
            # 2. message info from network
            assert head is None and body is None, 'params error: %s, %s, %s' % (msg, head, body)
            super().__init__(msg, head)
        # lazy
        self.__content = body

    @property  # Override
    def content(self) -> Content:
        if self.__content is None:
            info = self.get('content')
            self.__content = Content.parse(content=info)
            assert self.__content is not None, 'content error: %s' % info
        return self.__content

    @content.setter  # protected
    def content(self, value: Content):
        self.set_map(key='content', value=value)
        self.__content = value

    @property  # Override
    def time(self) -> Optional[DateTime]:
        value = self.content.time
        if value is not None:
            return value
        # return super().time
        return self.envelope.time

    @property  # Override
    def group(self) -> Optional[ID]:
        return self.content.group

    @property  # Override
    def type(self) -> Optional[str]:
        return self.content.type
