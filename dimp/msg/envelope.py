# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
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

import time as time_lib
from typing import Optional, Union, Any, Dict

from mkm.types import Dictionary
from mkm import ID, ANYONE

from dkd import ContentType
from dkd import Envelope, EnvelopeFactory


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
                 sender: ID = None, receiver: ID = None, time: float = None):
        if envelope is None:
            assert sender is not None, 'sender should not be empty'
            if receiver is None:
                receiver = ANYONE
            if time is None:
                time = time_lib.time()
            envelope = {
                'sender': str(sender),
                'receiver': str(receiver),
                'time': time,
            }
        # initialize with envelope info
        super().__init__(dictionary=envelope)
        # lazy load
        self.__sender = sender
        self.__receiver = receiver
        self.__time = time
        self.__group = None
        self.__type = None

    @property  # Override
    def sender(self) -> ID:
        if self.__sender is None:
            identifier = self.get(key='sender')
            self.__sender = ID.parse(identifier=identifier)
        return self.__sender

    @property  # Override
    def receiver(self) -> ID:
        if self.__receiver is None:
            identifier = self.get(key='receiver')
            if identifier is None:
                self.__receiver = ANYONE
            else:
                self.__receiver = ID.parse(identifier=identifier)
        return self.__receiver

    @property  # Override
    def time(self) -> float:
        if self.__time is None:
            self.__time = self.get_time(key='time')
        return self.__time

    @property  # Override
    def group(self) -> Optional[ID]:
        if self.__group is None:
            identifier = self.get(key='group')
            self.__group = ID.parse(identifier=identifier)
        return self.__group

    @group.setter  # Override
    def group(self, value: ID):
        if value is None:
            self.pop('group', None)
        else:
            self['group'] = str(value)
        self.__group = value

    @property  # Override
    def type(self) -> Optional[int]:
        if self.__type is None:
            self.__type = self.get_int('type')
        return self.__type

    @type.setter  # Override
    def type(self, value: Union[int, ContentType]):
        if isinstance(value, ContentType):
            value = value.value
        if value is None or value == 0:
            self.pop('type', None)
        else:
            self['type'] = value
        self.__type = value


class MessageEnvelopeFactory(EnvelopeFactory):

    # Override
    def create_envelope(self, sender: ID, receiver: ID, time: float) -> Envelope:
        return MessageEnvelope(sender=sender, receiver=receiver, time=time)

    # Override
    def parse_envelope(self, envelope: Dict[str, Any]) -> Optional[Envelope]:
        # check 'sender'
        if 'sender' in envelope:
            return MessageEnvelope(envelope=envelope)
        # env.sender should not be empty
