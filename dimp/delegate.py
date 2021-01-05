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
    Delegates
    ~~~~~~~~~

    Delegates for Transceiver, such as Barrack, KeyStore, FTP, ...
"""

from abc import ABC, abstractmethod
from typing import Optional, List

from mkm.crypto import SymmetricKey
from mkm import ID

from dkd import Content, InstantMessage, SecureMessage, ReliableMessage

from .user import User
from .group import Group


class EntityDelegate(ABC):

    @property
    @abstractmethod
    def local_users(self) -> Optional[List[User]]:
        """
        Get all local users (for decrypting received message)

        :return: users with private key
        """
        raise NotImplemented

    @abstractmethod
    def select_user(self, receiver: ID) -> Optional[User]:
        """
        Select local user for receiver

        :param receiver: user/group ID
        :return: local user
        """
        raise NotImplemented

    @abstractmethod
    def user(self, identifier: ID) -> Optional[User]:
        """
        Create user with ID

        :param identifier: ID object
        :return: User object
        """
        raise NotImplemented

    @abstractmethod
    def group(self, identifier: ID) -> Optional[Group]:
        """
        Create group with ID

        :param identifier: ID object
        :return: Group object
        """
        raise NotImplemented


class CipherKeyDelegate(ABC):

    @abstractmethod
    def cipher_key(self, sender: ID, receiver: ID, generate: bool=False) -> Optional[SymmetricKey]:
        """
        Get cipher key for encrypt message from 'sender' to 'receiver'

        :param sender:   user or contact ID
        :param receiver: contact or user/group ID
        :param generate: generate when key not exists
        :return:         cipher key
        """
        raise NotImplemented

    @abstractmethod
    def cache_cipher_key(self, key: SymmetricKey, sender: ID, receiver: ID):
        """
        Cache cipher key for reusing, with direction (from 'sender' to 'receiver')

        :param key:      cipher key from a contact
        :param sender:   user or contact ID
        :param receiver: contact or user/group ID
        """
        raise NotImplemented


class MessagePacker:

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


class MessageProcessor:

    @abstractmethod
    def process_package(self, data: bytes) -> Optional[bytes]:
        """
        Process data package

        :param data: data to be processed
        :return: response data
        """
        raise NotImplemented

    @abstractmethod
    def process_reliable_message(self, msg: ReliableMessage) -> Optional[ReliableMessage]:
        """
        Process network message

        :param msg: message to be processed
        :return: response message
        """
        raise NotImplemented

    @abstractmethod
    def process_secure_message(self, msg: SecureMessage, r_msg: ReliableMessage) -> Optional[SecureMessage]:
        """
        Process encrypted message

        :param msg:   message to be processed
        :param r_msg: message received
        :return: response message
        """
        raise NotImplemented

    @abstractmethod
    def process_instant_message(self, msg: InstantMessage, r_msg: ReliableMessage) -> Optional[InstantMessage]:
        """
        Process plain message

        :param msg:   message to be processed
        :param r_msg: message received
        :return: response message
        """
        raise NotImplemented

    @abstractmethod
    def process_content(self, content: Content, r_msg: ReliableMessage) -> Optional[Content]:
        """
        Process message content

        :param content: content to be processed
        :param r_msg: message received
        :return: response content
        """
        raise NotImplemented
