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

from abc import ABC
from typing import Optional

from mkm.crypto import base64_encode, base64_decode, utf8_encode, utf8_decode, json_encode, json_decode
from mkm.crypto import SymmetricKey
from mkm import ID

from dkd import Message
from dkd import InstantMessage, SecureMessage, ReliableMessage
from dkd import InstantMessageDelegate, ReliableMessageDelegate
from dkd import Content

from .mkm import EntityDelegate


class Transceiver(InstantMessageDelegate, ReliableMessageDelegate, ABC):
    """ Converting message format between PlainMessage and NetworkMessage """

    @property
    def barrack(self) -> EntityDelegate:
        raise NotImplemented

    #
    #   InstantMessageDelegate
    #

    # Override
    def serialize_content(self, content: Content, key: SymmetricKey, msg: InstantMessage) -> bytes:
        # NOTICE: check attachment for File/Image/Audio/Video message content
        #         before serialize content, this job should be do in subclass
        js = json_encode(obj=content.dictionary)
        return utf8_encode(string=js)

    # Override
    def encrypt_content(self, data: bytes, key: SymmetricKey, msg: InstantMessage) -> bytes:
        return key.encrypt(data=data)

    # Override
    def encode_data(self, data: bytes, msg: InstantMessage) -> str:
        if is_broadcast(msg=msg):
            # broadcast message content will not be encrypted (just encoded to JsON),
            # so no need to encode to Base64 here
            return utf8_decode(data=data)
        return base64_encode(data=data)

    # Override
    def serialize_key(self, key: SymmetricKey, msg: InstantMessage) -> Optional[bytes]:
        if is_broadcast(msg=msg):
            # broadcast message has no key
            return None
        js = json_encode(obj=key.dictionary)
        return utf8_encode(string=js)

    # Override
    def encrypt_key(self, data: bytes, receiver: ID, msg: InstantMessage) -> Optional[bytes]:
        assert not is_broadcast(msg=msg), 'broadcast message has no key: %s' % msg
        # TODO: make sure the receiver's public key exists
        contact = self.barrack.user(identifier=receiver)
        assert contact is not None, 'failed to encrypt for receiver: %s' % receiver
        # encrypt with receiver's public key
        return contact.encrypt(data=data)

    # Override
    def encode_key(self, data: bytes, msg: InstantMessage) -> str:
        assert not is_broadcast(msg=msg), 'broadcast message has no key: %s' % msg
        return base64_encode(data=data)

    #
    #   SecureMessageDelegate
    #

    # Override
    def decode_key(self, key: str, msg: SecureMessage) -> Optional[bytes]:
        assert not is_broadcast(msg=msg), 'broadcast message has no key'
        return base64_decode(string=key)

    # Override
    # noinspection PyUnusedLocal
    def decrypt_key(self, data: bytes, sender: ID, receiver: ID, msg: SecureMessage) -> Optional[bytes]:
        assert not is_broadcast(msg=msg), 'broadcast message has no key'
        # decrypt key data with the receiver's private key
        user = self.barrack.user(identifier=msg.receiver)
        assert user is not None, 'failed to create local user: %s' % msg.receiver
        return user.decrypt(data=data)

    # Override
    def deserialize_key(self, data: Optional[bytes], sender: ID, receiver: ID,
                        msg: SecureMessage) -> Optional[SymmetricKey]:
        # NOTICE: the receiver will be group ID in a group message here
        assert not is_broadcast(msg=msg), 'broadcast message has no key: %s' % msg
        js = utf8_decode(data=data)
        dictionary = json_decode(string=js)
        # TODO: translate short keys
        #       'A' -> 'algorithm'
        #       'D' -> 'data'
        #       'V' -> 'iv'
        #       'M' -> 'mode'
        #       'P' -> 'padding'
        return SymmetricKey.parse(key=dictionary)

    # Override
    def decode_data(self, data: str, msg: SecureMessage) -> Optional[bytes]:
        if is_broadcast(msg=msg):
            # broadcast message content will not be encrypted (just encoded to JsON),
            # so return the string data directly
            return utf8_encode(string=data)
        return base64_decode(string=data)

    # Override
    def decrypt_content(self, data: bytes, key: SymmetricKey, msg: SecureMessage) -> Optional[bytes]:
        return key.decrypt(data)

    # Override
    def deserialize_content(self, data: bytes, key: SymmetricKey, msg: SecureMessage) -> Optional[Content]:
        js = utf8_decode(data=data)
        dictionary = json_decode(string=js)
        # TODO: translate short keys
        #       'T' -> 'type'
        #       'N' -> 'sn'
        #       'G' -> 'group'
        return Content.parse(content=dictionary)

    # Override
    # noinspection PyUnusedLocal
    def sign_data(self, data: bytes, sender: ID, msg: SecureMessage) -> bytes:
        user = self.barrack.user(identifier=sender)
        assert user is not None, 'failed to sign with sender: %s' % sender
        return user.sign(data)

    # Override
    def encode_signature(self, signature: bytes, msg: SecureMessage) -> str:
        return base64_encode(data=signature)

    #
    #   ReliableMessageDelegate
    #

    # Override
    def decode_signature(self, signature: str, msg: ReliableMessage) -> Optional[bytes]:
        return base64_decode(string=signature)

    # Override
    def verify_data_signature(self, data: bytes, signature: bytes, sender: ID, msg: ReliableMessage) -> bool:
        user = self.barrack.user(identifier=sender)
        assert user is not None, 'failed to verify signature for sender: %s' % sender
        return user.verify(data=data, signature=signature)


def is_broadcast(msg: Message) -> bool:
    receiver = msg.group
    if receiver is None:
        receiver = msg.receiver
    return receiver.is_broadcast
