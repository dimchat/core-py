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
    DIMP - Message Contents
    ~~~~~~~~~~~~~~~~~~~~~~~
"""

import json
from typing import Optional

from mkm.crypto.utils import base64_encode, base64_decode
from mkm import SymmetricKey
from mkm import ID, LocalUser, is_broadcast
from dkd import IInstantMessageDelegate, IReliableMessageDelegate
from dkd import Content, Message, InstantMessage, SecureMessage, ReliableMessage

from .text import TextContent
from .file import FileContent, ImageContent, AudioContent, VideoContent

from .command import Command
from .history import HistoryCommand

from ..delegate import ISocialNetworkDataSource, ICipherKeyDataSource


__all__ = [
    'TextContent',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',

    'Command',
    'HistoryCommand',
    'Protocol',
]


class Protocol(IInstantMessageDelegate, IReliableMessageDelegate):

    def __init__(self):
        super().__init__()

        # delegates
        self.barrack: ISocialNetworkDataSource = None
        self.key_cache: ICipherKeyDataSource = None

    def is_broadcast_message(self, msg: Message) -> bool:
        receiver = self.barrack.identifier(msg.group)
        if receiver is None:
            receiver = self.barrack.identifier(msg.envelope.receiver)
        return is_broadcast(receiver)

    def serialize_content(self, content: Content, msg: InstantMessage) -> bytes:
        string = json.dumps(content)
        return string.encode('utf-8')

    def serialize_key(self, key: SymmetricKey, msg: InstantMessage) -> bytes:
        assert not self.is_broadcast_message(msg=msg), 'broadcast message has no key'
        string = json.dumps(key)
        return string.encode('utf-8')

    def deserialize_key(self, key: bytes, msg: SecureMessage) -> SymmetricKey:
        string = key.decode('utf-8')
        dictionary = json.loads(string)
        # TODO: translate short keys
        #       'A' -> 'algorithm'
        #       'D' -> 'data'
        #       'M' -> 'mode'
        #       'P' -> 'padding'
        return SymmetricKey(key=dictionary)

    def deserialize_content(self, data: bytes, msg: SecureMessage) -> Content:
        string = data.decode('utf-8')
        dictionary = json.loads(string)
        # TODO: translate short keys
        #       'S' -> 'sender'
        #       'R' -> 'receiver'
        #       'T' -> 'time'
        #       'D' -> 'data'
        #       'V' -> 'signature'
        #       'K' -> 'key'
        #       'M' -> 'meta'
        return Content(dictionary)

    #
    #   IInstantMessageDelegate
    #
    def encrypt_content(self, content: Content, key: dict, msg: InstantMessage) -> bytes:
        password = SymmetricKey(key=key)
        assert password == key, 'irregular symmetric key: %s' % key
        # encrypt with password
        data = self.serialize_content(content=content, msg=msg)
        return password.encrypt(data=data)

    def encode_data(self, data: bytes, msg: InstantMessage) -> str:
        if self.is_broadcast_message(msg=msg):
            # broadcast message content will not be encrypted (just encoded to JsON),
            # so no need to encode to Base64 here
            return data.decode('utf-8')
        # encode to Base64
        return base64_encode(data)

    def encrypt_key(self, key: dict, receiver: str, msg: InstantMessage) -> Optional[bytes]:
        if self.is_broadcast_message(msg=msg):
            # broadcast message has no key
            return None
        password = SymmetricKey(key=key)
        assert password == key, 'irregular symmetric key: %s' % key
        # TODO: check whether support reused key

        data = self.serialize_key(key=password, msg=msg)
        # encrypt with receiver's public key
        contact = self.barrack.user(identifier=self.barrack.identifier(receiver))
        assert contact is not None, 'failed to encrypt key for receiver: %s' % receiver
        return contact.encrypt(data=data)

    def encode_key(self, key: bytes, msg: InstantMessage) -> Optional[str]:
        assert not self.is_broadcast_message(msg=msg), 'broadcast message has no key'
        # encode to Base64
        return base64_encode(key)

    #
    #   ISecureMessageDelegate
    #
    def decode_key(self, key: str, msg: SecureMessage) -> Optional[bytes]:
        assert not self.is_broadcast_message(msg=msg), 'broadcast message has no key'
        # decode from Base64
        return base64_decode(key)

    def decrypt_key(self, key: bytes, sender: str, receiver: str, msg: SecureMessage) -> Optional[dict]:
        assert not self.is_broadcast_message(msg=msg) or key is None, 'broadcast message has no key'
        sender = self.barrack.identifier(sender)
        receiver = self.barrack.identifier(receiver)
        password = None
        if key is not None:
            # decrypt key data with the receiver's private key
            identifier = self.barrack.identifier(msg.envelope.receiver)
            user: LocalUser = self.barrack.user(identifier=identifier)
            assert user is not None, 'failed to decrypt key for receiver: %s, %s' % (receiver, identifier)
            plaintext = user.decrypt(data=key)
            if plaintext is None:
                raise AssertionError('failed to decrypt key in msg: %s' % msg)
            # deserialize it to symmetric key
            password = self.deserialize_key(key=plaintext, msg=msg)
            # cache the new key in key store
            self.key_cache.cache_cipher_key(key=password, sender=sender, receiver=receiver)
        if password is None:
            # if key data is empty, get it from key store
            password = self.key_cache.cipher_key(sender=sender, receiver=receiver)
            assert password is not None, 'failed to get password from %s to %s' % (sender, receiver)
        return password

    def decode_data(self, data: str, msg: SecureMessage) -> bytes:
        if self.is_broadcast_message(msg=msg):
            # broadcast message content will not be encrypted (just encoded to JsON),
            # so return the string data directly
            return data.encode('utf-8')
        # decode from Base64
        return base64_decode(data)

    def decrypt_content(self, data: bytes, key: dict, msg: SecureMessage) -> Content:
        password = SymmetricKey(key=key)
        assert password == key, 'irregular symmetric key: %s' % key
        plaintext = password.decrypt(data)
        if plaintext is not None:
            return self.deserialize_content(data=plaintext, msg=msg)

    def sign_data(self, data: bytes, sender: str, msg: SecureMessage) -> bytes:
        sender = self.barrack.identifier(sender)
        user: LocalUser = self.barrack.user(identifier=sender)
        assert user is not None, 'failed to sign with sender: %s' % sender
        return user.sign(data)

    def encode_signature(self, signature: bytes, msg: SecureMessage) -> str:
        return base64_encode(signature)

    #
    #   IReliableMessageDelegate
    #
    def decode_signature(self, signature: str, msg: ReliableMessage) -> bytes:
        return base64_decode(signature)

    def verify_data_signature(self, data: bytes, signature: bytes, sender: str, msg: ReliableMessage) -> bool:
        sender = self.barrack.identifier(sender)
        contact = self.barrack.user(identifier=sender)
        assert contact is not None, 'failed to verify with sender: %s' % sender
        return contact.verify(data=data, signature=signature)
