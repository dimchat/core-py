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

from typing import Optional, Any, Dict

from mkm.types import DateTime
from mkm.types import Dictionary
from mkm import ID, ANYONE

from dkd import Envelope


"""
    Envelope for message
    ~~~~~~~~~~~~~~~~~~~~
    This class is used to create a message envelope
    which contains 'sender', 'receiver' and 'time'
    
    data format: {
        sender   : "moki@xxx",
        receiver : "hulk@yyy",
        time     : 123
    }
"""


class MessageEnvelope(Dictionary, Envelope):

    def __init__(self, envelope: Dict[str, Any] = None,
                 sender: ID = None, receiver: Optional[ID] = None, time: Optional[DateTime] = None):
        if envelope is None:
            # 1. new envelope with sender, receiver & time
            assert sender is not None, 'envelope error: %s, %s' % (receiver, time)
            if receiver is None:
                receiver = ANYONE
            if time is None:
                time = DateTime.now()
            envelope = {
                'sender': str(sender),
                'receiver': str(receiver),
                'time': time.timestamp,
            }
        else:
            # 2. envelope info from network
            assert sender is None and receiver is None and time is None, \
                'params error: %s, %s, %s, %s' % (envelope, sender, receiver, time)
        # initialize with envelope info
        super().__init__(dictionary=envelope)
        # lazy load
        self.__sender = sender
        self.__receiver = receiver
        self.__time = time

    @property  # Override
    def sender(self) -> ID:
        if self.__sender is None:
            identifier = self.get('sender')
            self.__sender = ID.parse(identifier=identifier)
        return self.__sender

    @property  # Override
    def receiver(self) -> ID:
        if self.__receiver is None:
            identifier = self.get('receiver')
            identifier = ID.parse(identifier=identifier)
            if identifier is None:
                self.__receiver = ANYONE
            else:
                self.__receiver = identifier
        return self.__receiver

    @property  # Override
    def time(self) -> Optional[DateTime]:
        if self.__time is None:
            self.__time = self.get_datetime(key='time', default=None)
        return self.__time

    @property  # Override
    def group(self) -> Optional[ID]:
        identifier = self.get('group')
        return ID.parse(identifier=identifier)

    @group.setter  # Override
    def group(self, value: ID):
        self.set_string(key='group', value=value)

    @property  # Override
    def type(self) -> Optional[str]:
        return self.get_str(key='type', default=None)

    @type.setter  # Override
    def type(self, value: str):
        self['type'] = value
