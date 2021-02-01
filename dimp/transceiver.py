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
    Transceiver
    ~~~~~~~~~~~

    Delegate to process message transforming
"""

import weakref
from abc import abstractmethod
from typing import Optional

from mkm.crypto import base64_encode, base64_decode, utf8_encode, utf8_decode, json_encode, json_decode
from mkm.crypto import SymmetricKey
from mkm import ID

from dkd import Message
from dkd import InstantMessage, SecureMessage, ReliableMessage
from dkd import InstantMessageDelegate, ReliableMessageDelegate
from dkd import Content

from .delegate import EntityDelegate, CipherKeyDelegate
from .user import User
from .group import Group


class Transceiver(InstantMessageDelegate, ReliableMessageDelegate):

    def __init__(self):
        super().__init__()
        self.__barrack: Optional[weakref.ReferenceType] = None
        self.__key_cache: Optional[weakref.ReferenceType] = None
        self.__packer: Optional[weakref.ReferenceType] = None
        self.__processor: Optional[weakref.ReferenceType] = None

    @property
    def barrack(self) -> EntityDelegate:
        """ Barrack (EntityDelegate) """
        if self.__barrack is not None:
            return self.__barrack()

    @barrack.setter
    def barrack(self, delegate: EntityDelegate):
        self.__barrack = weakref.ref(delegate)

    @property
    def key_cache(self) -> CipherKeyDelegate:
        """ KeyCache (CipherKeyDelegate) """
        if self.__key_cache is not None:
            return self.__key_cache()

    @key_cache.setter
    def key_cache(self, delegate: CipherKeyDelegate):
        self.__key_cache = weakref.ref(delegate)

    #
    #   Interfaces for User/Group
    #
    def select_user(self, receiver: ID) -> Optional[User]:
        return self.barrack.select_user(receiver=receiver)

    def user(self, identifier: ID) -> Optional[User]:
        return self.barrack.user(identifier=identifier)

    def group(self, identifier: ID) -> Optional[Group]:
        return self.barrack.group(identifier=identifier)

    #
    #   Interfaces for Cipher Key
    #
    def cipher_key(self, sender: ID, receiver: ID, generate: bool = False) -> Optional[SymmetricKey]:
        return self.key_cache.cipher_key(sender=sender, receiver=receiver, generate=generate)

    def cache_cipher_key(self, key: SymmetricKey, sender: ID, receiver: ID):
        return self.key_cache.cache_cipher_key(key=key, sender=sender, receiver=receiver)

    #
    #   Message Packer
    #
    class Packer:

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

    @property
    def packer(self) -> Packer:
        """ Message Packer """
        if self.__packer is not None:
            return self.__packer()

    @packer.setter
    def packer(self, delegate: Packer):
        self.__packer = weakref.ref(delegate)

    #
    #   Interfaces for Packing Message
    #
    def overt_group(self, content: Content) -> Optional[ID]:
        return self.packer.overt_group(content=content)

    def encrypt_message(self, msg: InstantMessage) -> Optional[SecureMessage]:
        return self.packer.encrypt_message(msg=msg)

    def sign_message(self, msg: SecureMessage) -> ReliableMessage:
        return self.packer.sign_message(msg=msg)

    def serialize_message(self, msg: ReliableMessage) -> bytes:
        return self.packer.serialize_message(msg=msg)

    def deserialize_message(self, data: bytes) -> Optional[ReliableMessage]:
        return self.packer.deserialize_message(data=data)

    def verify_message(self, msg: ReliableMessage) -> Optional[SecureMessage]:
        return self.packer.verify_message(msg=msg)

    def decrypt_message(self, msg: SecureMessage) -> Optional[InstantMessage]:
        return self.packer.decrypt_message(msg=msg)

    #
    #   Message Processor
    #
    class Processor:

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

    @property
    def processor(self) -> Processor:
        """ Message Processor """
        if self.__processor is not None:
            return self.__processor()

    @processor.setter
    def processor(self, delegate: Processor):
        self.__processor = weakref.ref(delegate)

    #
    #   Interfaces for Processing Message
    #
    def process_package(self, data: bytes) -> Optional[bytes]:
        return self.processor.process_package(data=data)

    def process_reliable_message(self, msg: ReliableMessage) -> Optional[ReliableMessage]:
        return self.processor.process_reliable_message(msg=msg)

    def process_secure_message(self, msg: SecureMessage, r_msg: ReliableMessage) -> Optional[SecureMessage]:
        return self.processor.process_secure_message(msg=msg, r_msg=r_msg)

    def process_instant_message(self, msg: InstantMessage, r_msg: ReliableMessage) -> Optional[InstantMessage]:
        return self.processor.process_instant_message(msg=msg, r_msg=r_msg)

    def process_content(self, content: Content, r_msg: ReliableMessage) -> Optional[Content]:
        return self.processor.process_content(content=content, r_msg=r_msg)

    #
    #   InstantMessageDelegate
    #

    def serialize_content(self, content: Content, key: SymmetricKey, msg: InstantMessage) -> bytes:
        # NOTICE: check attachment for File/Image/Audio/Video message content
        #         before serialize content, this job should be do in subclass
        return json_encode(o=content.dictionary)

    def encrypt_content(self, data: bytes, key: SymmetricKey, msg: InstantMessage) -> bytes:
        return key.encrypt(data=data)

    def encode_data(self, data: bytes, msg: InstantMessage) -> str:
        if is_broadcast(msg=msg):
            # broadcast message content will not be encrypted (just encoded to JsON),
            # so no need to encode to Base64 here
            return utf8_decode(data=data)
        return base64_encode(data=data)

    def serialize_key(self, key: SymmetricKey, msg: InstantMessage) -> Optional[bytes]:
        if is_broadcast(msg=msg):
            # broadcast message has no key
            return None
        return json_encode(o=key.dictionary)

    def encrypt_key(self, data: bytes, receiver: ID, msg: InstantMessage) -> Optional[bytes]:
        assert not is_broadcast(msg=msg), 'broadcast message has no key: %s' % msg
        # TODO: make sure the receiver's public key exists
        contact = self.user(identifier=receiver)
        assert contact is not None, 'failed to encrypt for receiver: %s' % receiver
        # encrypt with receiver's public key
        return contact.encrypt(data=data)

    def encode_key(self, data: bytes, msg: InstantMessage) -> str:
        assert not is_broadcast(msg=msg), 'broadcast message has no key: %s' % msg
        return base64_encode(data=data)

    #
    #   SecureMessageDelegate
    #

    def decode_key(self, key: str, msg: SecureMessage) -> Optional[bytes]:
        assert not is_broadcast(msg=msg), 'broadcast message has no key'
        return base64_decode(string=key)

    # noinspection PyUnusedLocal
    def decrypt_key(self, data: bytes, sender: ID, receiver: ID, msg: SecureMessage) -> Optional[bytes]:
        assert not is_broadcast(msg=msg), 'broadcast message has no key'
        # decrypt key data with the receiver's private key
        user = self.user(identifier=msg.receiver)
        assert user is not None, 'failed to create local user: %s' % msg.receiver
        return user.decrypt(data=data)

    def deserialize_key(self, data: Optional[bytes], sender: ID, receiver: ID,
                        msg: SecureMessage) -> Optional[SymmetricKey]:
        if data is None:
            # get key from cache
            return self.cipher_key(sender=sender, receiver=receiver)
        else:
            assert not is_broadcast(msg=msg), 'broadcast message has no key: %s' % msg
            dictionary = json_decode(data=data)
            # TODO: translate short keys
            #       'A' -> 'algorithm'
            #       'D' -> 'data'
            #       'V' -> 'iv'
            #       'M' -> 'mode'
            #       'P' -> 'padding'
            return SymmetricKey.parse(key=dictionary)

    def decode_data(self, data: str, msg: SecureMessage) -> Optional[bytes]:
        if is_broadcast(msg=msg):
            # broadcast message content will not be encrypted (just encoded to JsON),
            # so return the string data directly
            return utf8_encode(string=data)
        return base64_decode(string=data)

    def decrypt_content(self, data: bytes, key: SymmetricKey, msg: SecureMessage) -> Optional[bytes]:
        return key.decrypt(data)

    def deserialize_content(self, data: bytes, key: SymmetricKey, msg: SecureMessage) -> Optional[Content]:
        dictionary = json_decode(data=data)
        # TODO: translate short keys
        #       'T' -> 'type'
        #       'N' -> 'sn'
        #       'G' -> 'group'
        content = Content.parse(content=dictionary)
        assert content is not None, 'content error: %d' % len(data)

        if not is_broadcast(msg=msg):
            # check and cache key for reuse
            group = self.overt_group(content=content)
            if group is None:
                # personal message or (group) command
                # cache key with direction (sender -> receiver)
                self.cache_cipher_key(key=key, sender=msg.sender, receiver=msg.receiver)
            else:
                # group message (excludes group command)
                # cache the key with direction (sender -> group)
                self.cache_cipher_key(key=key, sender=msg.sender, receiver=group)
        # NOTICE: check attachment for File/Image/Audio/Video message content
        #         after deserialize content, this job should be do in subclass
        return content

    # noinspection PyUnusedLocal
    def sign_data(self, data: bytes, sender: ID, msg: SecureMessage) -> bytes:
        user = self.user(identifier=sender)
        assert user is not None, 'failed to sign with sender: %s' % sender
        return user.sign(data)

    def encode_signature(self, signature: bytes, msg: SecureMessage) -> str:
        return base64_encode(data=signature)

    #
    #   ReliableMessageDelegate
    #

    def decode_signature(self, signature: str, msg: ReliableMessage) -> Optional[bytes]:
        return base64_decode(string=signature)

    def verify_data_signature(self, data: bytes, signature: bytes, sender: ID, msg: ReliableMessage) -> bool:
        contact = self.user(identifier=sender)
        assert contact is not None, 'failed to verify signature for sender: %s' % sender
        return contact.verify(data=data, signature=signature)


def is_broadcast(msg: Message) -> bool:
    receiver = msg.group
    if receiver is None:
        receiver = msg.receiver
    return receiver.is_broadcast
