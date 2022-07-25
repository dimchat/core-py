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

from typing import Optional, Any, Dict, List

from dkd import ContentType, BaseContent
from dkd import ReliableMessage

from ..protocol import ForwardContent


class SecretContent(BaseContent, ForwardContent):
    """
        Top-Secret Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0xFF,
            sn   : 456,

            forward : {...}  // reliable (secure + certified) message
            secrets : [...]  // reliable (secure + certified) messages
        }
    """

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 message: Optional[ReliableMessage] = None,
                 messages: Optional[List[ReliableMessage]] = None):
        if content is None:
            super().__init__(msg_type=ContentType.FORWARD)
        else:
            super().__init__(content=content)
        self.__forward = message
        self.__secrets = messages
        if message is not None:
            self['forward'] = message.dictionary
        if messages is not None:
            self['secrets'] = revert_messages(messages=messages)

    #
    #   forward (top-secret message)
    #
    @property  # Override
    def forward(self) -> ReliableMessage:
        if self.__forward is None:
            msg = self.get('forward')
            self.__forward = ReliableMessage.parse(msg=msg)
            # assert msg is not None, 'forward message not found: %s' % self.dictionary
        return self.__forward

    @property  # Override
    def secrets(self) -> List[ReliableMessage]:
        if self.__secrets is None:
            messages = self.get('secrets')
            if messages is None:
                # get from 'forward'
                self.__secrets = [self.forward]
            else:
                # get from 'secrets'
                self.__secrets = convert_messages(messages=messages)
        return self.__secrets


def convert_messages(messages: List[Dict[str, Any]]) -> List[ReliableMessage]:
    array = []
    for item in messages:
        msg = ReliableMessage.parse(msg=item)
        if msg is None:
            continue
        array.append(msg)
    return array


def revert_messages(messages: List[ReliableMessage]) -> List[Dict[str, Any]]:
    array = []
    for msg in messages:
        info = msg.dictionary
        array.append(info)
    return array
