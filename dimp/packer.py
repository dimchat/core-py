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

from abc import ABC, abstractmethod
from typing import Optional

from mkm import ID
from dkd import Content
from dkd import InstantMessage, SecureMessage, ReliableMessage


#
#   Message Packer
#
class Packer(ABC):

    @abstractmethod
    def overt_group(self, content: Content) -> Optional[ID]:
        """
        Get group ID which should be exposed to public network

        :param content: message content
        :return: exposed group ID
        """
        raise NotImplemented

    @abstractmethod
    def encrypt_message(self, msg: InstantMessage) -> Optional[SecureMessage]:
        """
        Encrypt message content

        :param msg: plain message
        :return: encrypted message
        """
        raise NotImplemented

    @abstractmethod
    def sign_message(self, msg: SecureMessage) -> ReliableMessage:
        """
        Sign content data

        :param msg: encrypted message
        :return: network message
        """
        raise NotImplemented

    @abstractmethod
    def serialize_message(self, msg: ReliableMessage) -> bytes:
        """
        Serialize network message

        :param msg: network message
        :return: data package
        """
        raise NotImplemented

    @abstractmethod
    def deserialize_message(self, data: bytes) -> Optional[ReliableMessage]:
        """
        Deserialize network message

        :param data: data package
        :return: network message
        """
        raise NotImplemented

    @abstractmethod
    def verify_message(self, msg: ReliableMessage) -> Optional[SecureMessage]:
        """
        Verify encrypted content data

        :param msg: network message
        :return: encrypted message
        """
        raise NotImplemented

    @abstractmethod
    def decrypt_message(self, msg: SecureMessage) -> Optional[InstantMessage]:
        """
        Decrypt message content

        :param msg: encrypted message
        :return: plain message
        """
        raise NotImplemented
