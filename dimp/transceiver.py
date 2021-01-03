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
from typing import Optional

from mkm.crypto import base64_encode, base64_decode, utf8_encode, utf8_decode, json_encode, json_decode
from mkm.crypto import SymmetricKey
from mkm import ID

from dkd import Message
from dkd import InstantMessage, SecureMessage, ReliableMessage
from dkd import InstantMessageDelegate, ReliableMessageDelegate
from dkd import Content

from .protocol import Command

from .delegate import EntityDelegate, CipherKeyDelegate


class Transceiver(InstantMessageDelegate, ReliableMessageDelegate):

    def __init__(self):
        super().__init__()
        self.__barrack: weakref.ReferenceType = None
        self.__key_cache: weakref.ReferenceType = None

    #
    #   Barrack (EntityDelegate)
    #
    @property
    def barrack(self) -> EntityDelegate:
        if self.__barrack is not None:
            return self.__barrack()

    @barrack.setter
    def barrack(self, value: EntityDelegate):
        if value is None:
            self.__barrack = None
        else:
            self.__barrack = weakref.ref(value)

    #
    #   KeyCache (CipherKeyDelegate)
    #
    @property
    def key_cache(self) -> CipherKeyDelegate:
        if self.__key_cache is not None:
            return self.__key_cache()

    @key_cache.setter
    def key_cache(self, value: CipherKeyDelegate):
        if value is None:
            self.__key_cache = None
        else:
            self.__key_cache = weakref.ref(value)

    def __is_broadcast(self, msg: Message) -> bool:
        if msg.delegate is None:
            msg.delegate = self
        receiver = msg.group
        if receiver is None:
            receiver = msg.receiver
        return receiver.is_broadcast

    #
    #   MessageDelegate
    #

    def overt_group(self, content: Content) -> Optional[ID]:
        group = content.group
        if group is not None:
            if group.is_broadcast:
                # broadcast message is always overt
                return group
            if isinstance(content, Command):
                # group command should be sent to each member directly, so
                # don't expose group ID
                return None
            return group

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
        if self.__is_broadcast(msg=msg):
            # broadcast message content will not be encrypted (just encoded to JsON),
            # so no need to encode to Base64 here
            return utf8_decode(data=data)
        return base64_encode(data=data)

    def serialize_key(self, key: SymmetricKey, msg: InstantMessage) -> Optional[bytes]:
        if self.__is_broadcast(msg=msg):
            # broadcast message has no key
            return None
        return json_encode(o=key.dictionary)

    def encrypt_key(self, data: bytes, receiver: ID, msg: InstantMessage) -> Optional[bytes]:
        assert not self.__is_broadcast(msg=msg), 'broadcast message has no key: %s' % msg
        # TODO: make sure the receiver's public key exists
        contact = self.barrack.user(identifier=receiver)
        assert contact is not None, 'failed to encrypt for receiver: %s' % receiver
        # encrypt with receiver's public key
        return contact.encrypt(data=data)

    def encode_key(self, data: bytes, msg: InstantMessage) -> str:
        assert not self.__is_broadcast(msg=msg), 'broadcast message has no key: %s' % msg
        return base64_encode(data=data)

    #
    #   SecureMessageDelegate
    #

    def decode_key(self, key: str, msg: SecureMessage) -> Optional[bytes]:
        assert not self.__is_broadcast(msg=msg), 'broadcast message has no key'
        return base64_decode(string=key)

    # noinspection PyUnusedLocal
    def decrypt_key(self, data: bytes, sender: ID, receiver: ID, msg: SecureMessage) -> Optional[bytes]:
        assert not self.__is_broadcast(msg=msg), 'broadcast message has no key'
        # decrypt key data with the receiver's private key
        user = self.barrack.user(identifier=msg.receiver)
        assert user is not None, 'failed to create local user: %s' % msg.receiver
        return user.decrypt(data=data)

    def deserialize_key(self, data: Optional[bytes], sender: ID, receiver: ID,
                        msg: SecureMessage) -> Optional[SymmetricKey]:
        if data is None:
            # get key from cache
            return self.key_cache.cipher_key(sender=sender, receiver=receiver)
        else:
            assert not self.__is_broadcast(msg=msg), 'broadcast message has no key: %s' % msg
            dictionary = json_decode(data=data)
            # TODO: translate short keys
            #       'A' -> 'algorithm'
            #       'D' -> 'data'
            #       'V' -> 'iv'
            #       'M' -> 'mode'
            #       'P' -> 'padding'
            return SymmetricKey.parse(key=dictionary)

    def decode_data(self, data: str, msg: SecureMessage) -> Optional[bytes]:
        if self.__is_broadcast(msg=msg):
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

        if not self.__is_broadcast(msg=msg):
            # check and cache key for reuse
            group = self.overt_group(content=content)
            if group is None:
                # personal message or (group) command
                # cache key with direction (sender -> receiver)
                self.key_cache.cache_cipher_key(key=key, sender=msg.sender, receiver=msg.receiver)
            else:
                # group message (excludes group command)
                # cache the key with direction (sender -> group)
                self.key_cache.cache_cipher_key(key=key, sender=msg.sender, receiver=group)
        # NOTICE: check attachment for File/Image/Audio/Video message content
        #         after deserialize content, this job should be do in subclass
        return content

    # noinspection PyUnusedLocal
    def sign_data(self, data: bytes, sender: ID, msg: SecureMessage) -> bytes:
        user = self.barrack.user(identifier=sender)
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
        contact = self.barrack.user(identifier=sender)
        assert contact is not None, 'failed to verify signature for sender: %s' % sender
        return contact.verify(data=data, signature=signature)
