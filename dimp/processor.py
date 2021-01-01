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
from abc import abstractmethod
from typing import Optional

from dkd import Content, Envelope
from dkd import InstantMessage, SecureMessage, ReliableMessage
from dkd import MessageDelegate

from .delegate import EntityDelegate
from .packer import Packer


class Processor:

    def __init__(self, barrack: EntityDelegate, transceiver: MessageDelegate, packer: Packer):
        super().__init__()
        self.__barrack = weakref.ref(barrack)
        self.__transceiver = weakref.ref(transceiver)
        self.__packer = weakref.ref(packer)

    @property
    def barrack(self) -> EntityDelegate:
        return self.__barrack()

    @property
    def transceiver(self) -> MessageDelegate:
        return self.__transceiver()

    @property
    def packer(self) -> Packer:
        return self.__packer()

    #
    #  Processing Message
    #

    def process_package(self, data: bytes) -> Optional[bytes]:
        # 1. deserialize message
        r_msg = self.packer.deserialize_message(data=data)
        if r_msg is None:
            # no valid message received
            return None
        # 2. process message
        r_msg = self.process_reliable_message(r_msg=r_msg)
        if r_msg is None:
            # nothing to respond
            return None
        # 3. serialize message
        return self.packer.serialize_message(msg=r_msg)

    # TODO: override to check broadcast message before calling it
    # TODO: override to deliver to the receiver when catch exception "receiver error ..."
    def process_reliable_message(self, r_msg: ReliableMessage) -> Optional[ReliableMessage]:
        # 1. verify message
        s_msg = self.packer.verify_message(msg=r_msg)
        if s_msg is None:
            # waiting for sender's meta if not exists
            return None
        # 2. process message
        s_msg = self.process_secure_message(s_msg=s_msg, r_msg=r_msg)
        if s_msg is None:
            # nothing to respond
            return None
        # 3. sign message
        return self.packer.sign_message(msg=s_msg)

    def process_secure_message(self, s_msg: SecureMessage, r_msg: ReliableMessage) -> Optional[SecureMessage]:
        # 1. decrypt message
        i_msg = self.packer.decrypt_message(msg=s_msg)
        if i_msg is None:
            # cannot decrypt this message, not for you?
            # delivering message to other receiver?
            return None
        # 2. process message
        i_msg = self.process_instant_message(i_msg=i_msg, r_msg=r_msg)
        if i_msg is None:
            # nothing to respond
            return None
        # 3. encrypt message
        return self.packer.encrypt_message(msg=i_msg)

    def process_instant_message(self, i_msg: InstantMessage, r_msg: ReliableMessage) -> Optional[InstantMessage]:
        # process content from sender
        res = self.process_content(content=i_msg.content, r_msg=r_msg)
        if res is None:
            # nothing to respond
            return None
        user = self.barrack.select_user(receiver=i_msg.receiver)
        if user is None:
            raise AssertionError('receiver error: %s' % i_msg.receiver)
        # pack message
        env = Envelope.create(sender=user.identifier, receiver=i_msg.sender)
        return InstantMessage.create(head=env, body=res)

    @abstractmethod
    def process_content(self, content: Content, r_msg: ReliableMessage) -> Optional[Content]:
        raise NotImplemented
