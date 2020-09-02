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

from dkd import ContentType
from dkd import ReliableMessage

from .content import Content


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

    def __new__(cls, content: dict):
        """
        Create forward message content

        :param content: content info
        :return: ForwardContent object
        """
        if content is None:
            return None
        elif cls is ForwardContent:
            if isinstance(content, ForwardContent):
                # return ForwardContent object directly
                return content
        # new ForwardContent(dict)
        return super().__new__(cls, content)

    def __init__(self, content: dict):
        if self is content:
            # no need to init again
            return
        super().__init__(content)
        # lazy
        self.__forward: ReliableMessage = None

    #
    #   forward (top-secret message)
    #
    @property
    def message(self) -> ReliableMessage:
        if self.__forward is None:
            self.__forward = ReliableMessage(self.get('forward'))
        return self.__forward

    @message.setter
    def message(self, value: dict):
        if value is None:
            self.pop('forward', None)
        else:
            self['forward'] = value
        self.__forward = value

    #
    #   Factory
    #
    @classmethod
    def new(cls, content: dict=None, message: ReliableMessage=None, time: int=0):
        """
        Create forward message content with 'forward' (top-secret) message

        :param content: content info
        :param message: top-secret message
        :param time: message time
        :return: ForwardMessage object
        """
        if content is None:
            # create empty content
            content = {}
        # set 'forward' message
        if message is not None:
            content['forward'] = message
        # new ForwardContent(dict)
        return super().new(content=content, content_type=ContentType.Forward, time=time)


# register content class with type
Content.register(content_type=ContentType.Forward, content_class=ForwardContent)
