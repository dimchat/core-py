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

from typing import Optional

from dkd import ContentType, BaseContent
from dkd import ReliableMessage


class ForwardContent(BaseContent):
    """
        Top-Secret Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0xFF,
            sn   : 456,

            forward : {...}  // reliable (secure + certified) message
        }
    """

    def __init__(self, content: Optional[dict] = None, message: Optional[ReliableMessage] = None):
        if content is None:
            super().__init__(content_type=ContentType.FORWARD)
        else:
            super().__init__(content=content)
        self.__forward = None
        if message is not None:
            self.message = message

    #
    #   forward (top-secret message)
    #
    @property
    def message(self) -> ReliableMessage:
        if self.__forward is None:
            self.__forward = ReliableMessage.parse(msg=self.get('forward'))
        return self.__forward

    @message.setter
    def message(self, secret: ReliableMessage):
        self.__forward = secret
        if secret is None:
            self.pop('forward', None)
        else:
            self['forward'] = secret.dictionary
