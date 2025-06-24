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
    Message Transforming
    ~~~~~~~~~~~~~~~~~~~~

        Instant Message <-> Secure Message <-> Reliable Message
        +-------------+     +------------+     +--------------+
        |  sender     |     |  sender    |     |  sender      |
        |  receiver   |     |  receiver  |     |  receiver    |
        |  time       |     |  time      |     |  time        |
        |             |     |            |     |              |
        |  content    |     |  data      |     |  data        |
        +-------------+     |  key/keys  |     |  key/keys    |
                            +------------+     |  signature   |
                                               +--------------+
        Algorithm:
            data      = password.encrypt(content)
            key       = receiver.public_key.encrypt(password)
            signature = sender.private_key.sign(data)
"""


from typing import Optional, Any, Dict

from mkm.types import DateTime
from mkm.types import Dictionary
from mkm import ID

from dkd import Envelope, Message


class BaseMessage(Dictionary, Message):

    def __init__(self, msg: Dict[str, Any] = None, head: Envelope = None):
        if msg is None:
            # 1. new message with envelope
            assert head is not None, 'message envelope should not be empty'
            msg = head.dictionary
        else:
            # 2. message info from network
            assert head is None, 'params error: %s, %s' % (msg, head)
        super().__init__(dictionary=msg)
        # lazy
        self.__envelope = head

    @property  # Override
    def envelope(self) -> Envelope:
        if self.__envelope is None:
            # let envelope share the same dictionary with message
            self.__envelope = Envelope.parse(envelope=self.dictionary)
        return self.__envelope

    @property  # Override
    def sender(self) -> ID:
        return self.envelope.sender

    @property  # Override
    def receiver(self) -> ID:
        return self.envelope.receiver

    @property  # Override
    def time(self) -> Optional[DateTime]:
        return self.envelope.time

    @property  # Override
    def group(self) -> Optional[ID]:
        return self.envelope.group

    @property  # Override
    def type(self) -> Optional[str]:
        return self.envelope.type

    @classmethod
    def is_broadcast(cls, msg: Message) -> bool:
        if msg.receiver.is_broadcast:
            return True
        # check exposed group
        overt_group = msg.get('group')
        if overt_group is None:
            return False
        group = ID.parse(identifier=overt_group)
        return group is not None and group.is_broadcast
