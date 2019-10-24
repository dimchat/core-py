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

import json
from typing import Optional

from mkm.crypto.utils import base64_encode, base64_decode
from mkm import SymmetricKey, ID, is_broadcast
from mkm import LocalUser

from dkd import Content, Message
from dkd import InstantMessage, SecureMessage, ReliableMessage
from dkd import IInstantMessageDelegate, IReliableMessageDelegate

from .protocol import FileContent
from .delegate import ISocialNetworkDataSource, ICipherKeyDataSource, ITransceiverDelegate


class Transceiver(IInstantMessageDelegate, IReliableMessageDelegate):

    def __init__(self):
        super().__init__()

        # delegates
        self.barrack: ISocialNetworkDataSource = None
        self.key_cache: ICipherKeyDataSource = None
        self.delegate: ITransceiverDelegate = None

    def is_broadcast_message(self, msg: Message) -> bool:
        if isinstance(msg, InstantMessage):
            receiver = msg.content.group
        else:
            receiver = msg.envelope.group
        if receiver is None:
            receiver = msg.envelope.receiver
        identifier = self.barrack.identifier(receiver)
        return is_broadcast(identifier)

    def __password(self, sender: ID, receiver: ID) -> SymmetricKey:
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

    #
    #  Transform
    #
    def encrypt_message(self, msg: InstantMessage) -> SecureMessage:
        sender = self.barrack.identifier(msg.envelope.sender)
        receiver = self.barrack.identifier(msg.envelope.receiver)
        # if 'group' exists and the 'receiver' is a group ID,
        # they must be equal
        group = self.barrack.identifier(msg.content.group)
        # 1. get symmetric key
        if group is None:
            password = self.__password(sender=sender, receiver=receiver)
        else:
            # group message
            password = self.__password(sender=sender, receiver=group)
        if msg.delegate is None:
            msg.delegate = self
        assert msg.content is not None, 'message content empty: %s' % msg
        # 2. encrypt 'content' to 'data' for receiver/group members
        if receiver.type.is_group():
            # group message
            grp = self.barrack.group(identifier=receiver)
            s_msg = msg.encrypt(password=password, members=grp.members)
        else:
            # personal message (or split group message)
            assert receiver.type.is_user(), 'unknown receiver type: %s' % receiver
            s_msg = msg.encrypt(password=password)
        # OK
        return s_msg

    def sign_message(self, msg: SecureMessage) -> ReliableMessage:
        if msg.delegate is None:
            msg.delegate = self
        assert msg.data is not None, 'message data empty: %s' % msg
        # 1. sign 'data' by sender
        r_msg = msg.sign()
        # OK
        return r_msg

    def verify_message(self, msg: ReliableMessage) -> SecureMessage:
        # TODO: check [Meta Protocol]
        #       make sure the sender's meta exists
        #       (do in by application)

        if msg.delegate is None:
            msg.delegate = self
        assert msg.signature is not None, 'message signature empty: %s' % msg
        # 1. verify 'data' with 'signature'
        s_msg = msg.verify()

        # OK
        return s_msg

    def decrypt_message(self, msg: SecureMessage) -> InstantMessage:
        # NOTICE: make sure the receiver is YOU!
        #         which means the receiver's private key exists;
        #         if the receiver is a group ID, split it first

        if msg.delegate is None:
            msg.delegate = self
        assert msg.data is not None, 'message data empty: %s' % msg
        # 1. decrypt 'data' to 'content'
        i_msg = msg.decrypt()

        # TODO: check top-secret message
        #       (do it by application)

        # OK
        return i_msg

    #
    #  De/serialize message content and symmetric key
    #
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
        # check attachment for File/Image/Audio/Video message content before
        if isinstance(content, FileContent):
            data = password.encrypt(data=content.data)
            # upload (encrypted) file data onto CDN and save the URL in message content
            url = self.delegate.upload_data(data=data, msg=msg)
            if url is not None:
                content.url = url
                content.data = None
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
        if plaintext is None:
            raise ValueError('failed to decrypt data: %s, password: %s' % (data, password))
        content = self.deserialize_content(data=plaintext, msg=msg)

        # check attachment for File/Image/Audio/Video message content after
        if isinstance(content, FileContent):
            i_msg = InstantMessage.new(content=content, envelope=msg.envelope)
            # download from CDN
            file_data = self.delegate.download_data(content.url, i_msg)
            if file_data is None:
                # save symmetric key for decrypted file data after download from CDN
                content.password = password
            else:
                # decrypt file data
                content.data = password.decrypt(data=file_data)
                assert content.data is not None, 'failed to decrypt file data with key: %s' % key
                content.url = None
        return content

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
