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

    def load_password(self, sender: ID, receiver: ID) -> SymmetricKey:
        # 1. get old key from store
        old_key = self.key_cache.cipher_key(sender=sender, receiver=receiver)
        # 2. get new key from delegate
        new_key = self.key_cache.reuse_cipher_key(key=old_key, sender=sender, receiver=receiver)
        if new_key is None:
            if old_key is None:
                # 3. create a new key
                new_key = SymmetricKey(key={'algorithm': 'AES'})
            else:
                new_key = old_key
        # 4. update new key into the key store
        if new_key != old_key:
            self.key_cache.cache_cipher_key(key=new_key, sender=sender, receiver=receiver)
        return new_key

    def save_password(self, password: dict, sender: ID, receiver: ID) -> SymmetricKey:
        key = SymmetricKey(password)
        if key is not None:
            # cache the new key in key store
            self.key_cache.cache_cipher_key(key=key, sender=sender, receiver=receiver)
        return key

    #
    #   IInstantMessageDelegate
    #
    def encrypt_content(self, content: Content, key: dict, msg: InstantMessage) -> bytes:
        password = SymmetricKey(key)
        if password is None:
            raise AssertionError('failed to get symmetric key: %s' % key)
        # encrypt with password
        string = json.dumps(content)
        return password.encrypt(data=string.encode('utf-8'))

    def encode_content_data(self, data: bytes, msg: InstantMessage) -> str:
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
        # TODO: check whether support reused key

        # encrypt with receiver's public key
        receiver = self.barrack.identifier(receiver)
        contact = self.barrack.user(identifier=receiver)
        if contact is not None:
            string = json.dumps(key)
            return contact.encrypt(data=string.encode('utf-8'))

    def encode_key_data(self, key: bytes, msg: InstantMessage) -> Optional[str]:
        assert not self.is_broadcast_message(msg=msg) or key is None, 'broadcast message has no key'
        # encode to Base64
        if key is not None:
            return base64_encode(key)

    #
    #   ISecureMessageDelegate
    #
    def decrypt_key(self, key: bytes, sender: str, receiver: str, msg: SecureMessage) -> Optional[dict]:
        assert not self.is_broadcast_message(msg=msg) or key is None, 'broadcast message has no key'
        sender = self.barrack.identifier(sender)
        receiver = self.barrack.identifier(receiver)
        password = None
        if key is not None:
            # decrypt key data with the receiver's private key
            identifier = self.barrack.identifier(msg.envelope.receiver)
            user: LocalUser = self.barrack.user(identifier=identifier)
            data = user.decrypt(data=key)
            if data is None:
                raise AssertionError('failed to decrypt key data')
            # create symmetric key from JsON data
            pw = json.loads(data.decode('utf-8'))
            password = self.save_password(password=pw, sender=sender, receiver=receiver)
        if password is None:
            # if key data is empty, get it from key store
            password = self.key_cache.cipher_key(sender=sender, receiver=receiver)
        return password

    def decode_key_data(self, key: str, msg: SecureMessage) -> Optional[bytes]:
        assert not self.is_broadcast_message(msg=msg) or key is None, 'broadcast message has no key'
        # decode from Base64
        if key is not None:
            return base64_decode(key)

    def decrypt_content(self, data: bytes, key: dict, msg: SecureMessage) -> Content:
        password = SymmetricKey(key=key)
        if password is not None:
            plaintext = password.decrypt(data)
            if plaintext is not None:
                content = Content(json.loads(plaintext))
                return content

    def decode_content_data(self, data: str, msg: SecureMessage) -> bytes:
        if self.is_broadcast_message(msg=msg):
            # broadcast message content will not be encrypted (just encoded to JsON),
            # so return the string data directly
            return data.encode('utf-8')
        # decode from Base64
        return base64_decode(data)

    def sign_data(self, data: bytes, sender: str, msg: SecureMessage) -> bytes:
        sender = self.barrack.identifier(sender)
        user: LocalUser = self.barrack.user(identifier=sender)
        if user is not None:
            return user.sign(data)

    def encode_signature(self, signature: bytes, msg: SecureMessage) -> str:
        return base64_encode(signature)

    #
    #   IReliableMessageDelegate
    #
    def verify_data_signature(self, data: bytes, signature: bytes, sender: str, msg: ReliableMessage) -> bool:
        sender = self.barrack.identifier(sender)
        contact = self.barrack.user(identifier=sender)
        if contact is not None:
            return contact.verify(data=data, signature=signature)

    def decode_signature(self, signature: str, msg: ReliableMessage) -> bytes:
        return base64_decode(signature)
