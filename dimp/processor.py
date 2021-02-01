# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2020 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2020 Albert Moky
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

import weakref
from abc import ABC
from typing import Optional

from dkd import Envelope, InstantMessage, SecureMessage, ReliableMessage

from .transceiver import Transceiver


class Processor(Transceiver.Processor, ABC):

    def __init__(self, transceiver: Transceiver):
        super().__init__()
        self.__transceiver = weakref.ref(transceiver)

    @property
    def transceiver(self) -> Transceiver:
        return self.__transceiver()

    #
    #  Processing Message
    #

    def process_package(self, data: bytes) -> Optional[bytes]:
        # 1. deserialize message
        msg = self.transceiver.deserialize_message(data=data)
        if msg is None:
            # no valid message received
            return None
        # 2. process message
        msg = self.transceiver.process_reliable_message(msg=msg)
        if msg is None:
            # nothing to respond
            return None
        # 3. serialize message
        return self.transceiver.serialize_message(msg=msg)

    def process_reliable_message(self, msg: ReliableMessage) -> Optional[ReliableMessage]:
        # TODO: override to check broadcast message before calling it
        # 1. verify message
        s_msg = self.transceiver.verify_message(msg=msg)
        if s_msg is None:
            # waiting for sender's meta if not exists
            return None
        # 2. process message
        s_msg = self.transceiver.process_secure_message(msg=s_msg, r_msg=msg)
        if s_msg is None:
            # nothing to respond
            return None
        # 3. sign message
        return self.transceiver.sign_message(msg=s_msg)
        # TODO: override to deliver to the receiver when catch exception "receiver error ..."

    def process_secure_message(self, msg: SecureMessage, r_msg: ReliableMessage) -> Optional[SecureMessage]:
        # 1. decrypt message
        i_msg = self.transceiver.decrypt_message(msg=msg)
        if i_msg is None:
            # cannot decrypt this message, not for you?
            # delivering message to other receiver?
            return None
        # 2. process message
        i_msg = self.transceiver.process_instant_message(msg=i_msg, r_msg=r_msg)
        if i_msg is None:
            # nothing to respond
            return None
        # 3. encrypt message
        return self.transceiver.encrypt_message(msg=i_msg)

    def process_instant_message(self, msg: InstantMessage, r_msg: ReliableMessage) -> Optional[InstantMessage]:
        # process content from sender
        res = self.transceiver.process_content(content=msg.content, r_msg=r_msg)
        if res is None:
            # nothing to respond
            return None
        user = self.transceiver.select_user(receiver=msg.receiver)
        if user is None:
            raise AssertionError('receiver error: %s' % msg.receiver)
        # pack message
        env = Envelope.create(sender=user.identifier, receiver=msg.sender)
        return InstantMessage.create(head=env, body=res)
