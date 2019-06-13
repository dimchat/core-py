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

from dkd import Content, ReliableMessage
from dkd.content import message_content_classes

from .types import MessageType


class ForwardContent(Content):
    """
        Top-Secret Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0xFF,
            sn   : 456,

            forward : {...}  // reliable (secure + certified) message
        }
    """

    def __init__(self, content: dict):
        super().__init__(content)
        # 'forward'
        forward = content.get('forward')
        self.__forward = ReliableMessage(forward)

    #
    #   forward (top-secret message)
    #
    @property
    def forward(self) -> ReliableMessage:
        return self.__forward

    @forward.setter
    def forward(self, value: dict):
        self.__forward = value
        if value:
            self['forward'] = value
        else:
            self.pop('forward')

    #
    #   Factory
    #
    @classmethod
    def new(cls, message: ReliableMessage) -> Content:
        content = {
            'type': MessageType.Forward,
            'forward': message,
        }
        return ForwardContent(content)


message_content_classes[MessageType.Forward] = ForwardContent
