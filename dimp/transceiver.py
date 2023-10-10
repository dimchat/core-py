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

from abc import ABC, abstractmethod
from typing import Optional

from mkm.format import utf8_encode, utf8_decode, json_encode, json_decode
from mkm.crypto import SymmetricKey
from mkm import ID

from dkd import InstantMessage, SecureMessage, ReliableMessage
from dkd import InstantMessageDelegate, SecureMessageDelegate, ReliableMessageDelegate
from dkd import Content

from .mkm import EntityDelegate
from .msg import BaseMessage


class Transceiver(InstantMessageDelegate, SecureMessageDelegate, ReliableMessageDelegate, ABC):
    """ Converting message format between PlainMessage and NetworkMessage """

    @property
    @abstractmethod
    def barrack(self) -> Optional[EntityDelegate]:
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
        # store 'IV' in msg for AES encryption
        return key.encrypt(data=data, extra=msg.dictionary)

    # # Override
    # def encode_data(self, data: bytes, msg: InstantMessage) -> Any:
    #     if BaseMessage.is_broadcast(msg=msg):
    #         # broadcast message content will not be encrypted (just encoded to JsON),
    #         # so no need to encode to Base64 here
    #         return utf8_decode(data=data)
    #     # message content had been encrypted by a symmetric key,
    #     # so the data should be encoded here (with algorithm 'base64' as default).
    #     return TransportableData.encode(data=data)

    # Override
    def serialize_key(self, key: SymmetricKey, msg: InstantMessage) -> Optional[bytes]:
        if BaseMessage.is_broadcast(msg=msg):
            # broadcast message has no key
            return None
        js = json_encode(obj=key.dictionary)
        return utf8_encode(string=js)

    # Override
    def encrypt_key(self, data: bytes, receiver: ID, msg: InstantMessage) -> Optional[bytes]:
        assert not BaseMessage.is_broadcast(msg=msg), 'broadcast message has no key: %s' % msg
        assert receiver.is_user, 'receiver error: %s' % receiver
        # TODO: make sure the receiver's public key exists
        contact = self.barrack.user(identifier=receiver)
        if contact is None:
            assert False, 'failed to encrypt message key for receiver: %s' % receiver
        else:
            # encrypt with public key of the receiver (or group member)
            return contact.encrypt(data=data)

    # # Override
    # def encode_key(self, data: bytes, msg: InstantMessage) -> Any:
    #     assert not BaseMessage.is_broadcast(msg=msg), 'broadcast message has no key: %s' % msg
    #     # message key had been encrypted by a public key,
    #     # so the data should be encode here (with algorithm 'base64' as default).
    #     return TransportableData.encode(data=data)

    #
    #   SecureMessageDelegate
    #

    # # Override
    # def decode_key(self, key: Any, msg: SecureMessage) -> Optional[bytes]:
    #     assert not BaseMessage.is_broadcast(msg=msg), 'broadcast message has no key: %s' % msg
    #     return TransportableData.decode(key)

    # Override
    def decrypt_key(self, data: bytes, receiver: ID, msg: SecureMessage) -> Optional[bytes]:
        # NOTICE: the receiver must be a member ID
        #         if it's a group message
        assert not BaseMessage.is_broadcast(msg=msg), 'broadcast message has no key'
        assert receiver.is_user, 'receiver error: %s' % receiver
        user = self.barrack.user(identifier=receiver)
        if user is None:
            assert False, 'failed to create local user: %s' % msg.receiver
        else:
            # decrypt with private key of the receiver (or group member)
            return user.decrypt(data=data)

    # Override
    def deserialize_key(self, data: Optional[bytes], msg: SecureMessage) -> Optional[SymmetricKey]:
        assert not BaseMessage.is_broadcast(msg=msg), 'broadcast message has no key: %s' % msg
        if data is None:
            # assert False, 'reused key? get it from cache: %s => %s, %s' % (msg.sender, msg.receiver, msg.group)
            return None
        js = utf8_decode(data=data)
        if js is None:
            # assert False, 'message key data error: %s' % data
            return None
        dictionary = json_decode(string=js)
        # TODO: translate short keys
        #       'A' -> 'algorithm'
        #       'D' -> 'data'
        #       'V' -> 'iv'
        #       'M' -> 'mode'
        #       'P' -> 'padding'
        return SymmetricKey.parse(key=dictionary)

    # # Override
    # def decode_data(self, data: Any, msg: SecureMessage) -> Optional[bytes]:
    #     if BaseMessage.is_broadcast(msg=msg):
    #         # broadcast message content will not be encrypted (just encoded to JsON),
    #         # so return the string data directly
    #         if isinstance(data, str):
    #             return utf8_encode(string=data)
    #         else:
    #             # assert False, 'content data error: %s' % data
    #             return None
    #     else:
    #         # message content had been encrypted by a symmetric key,
    #         # so the data should be encoded here (with algorithm 'base64' as default).
    #         return TransportableData.decode(data)

    # Override
    def decrypt_content(self, data: bytes, key: SymmetricKey, msg: SecureMessage) -> Optional[bytes]:
        # check 'IV' in msg for AES decryption
        return key.decrypt(data=data, params=msg.dictionary)

    # Override
    def deserialize_content(self, data: bytes, key: SymmetricKey, msg: SecureMessage) -> Optional[Content]:
        js = utf8_decode(data=data)
        if js is None:
            # assert False, 'content data error: %s' % data
            return None
        dictionary = json_decode(string=js)
        # TODO: translate short keys
        #       'T' -> 'type'
        #       'N' -> 'sn'
        #       'W' -> 'time'
        #       'G' -> 'group'
        return Content.parse(content=dictionary)

    # Override
    # noinspection PyUnusedLocal
    def sign_data(self, data: bytes, msg: SecureMessage) -> bytes:
        sender = msg.sender
        user = self.barrack.user(identifier=sender)
        if user is None:
            assert False, 'failed to sign message data for sender: %s' % sender
        else:
            return user.sign(data)

    # # Override
    # def encode_signature(self, signature: bytes, msg: SecureMessage) -> str:
    #     return TransportableData.encode(data=signature)

    #
    #   ReliableMessageDelegate
    #

    # # Override
    # def decode_signature(self, signature: Any, msg: ReliableMessage) -> Optional[bytes]:
    #     return TransportableData.decode(signature)

    # Override
    def verify_data_signature(self, data: bytes, signature: bytes, msg: ReliableMessage) -> bool:
        sender = msg.sender
        contact = self.barrack.user(identifier=sender)
        if contact is None:
            assert False, 'failed to verify signature for sender: %s' % sender
        else:
            return contact.verify(data=data, signature=signature)
