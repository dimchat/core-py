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
import weakref
from typing import Optional

from mkm.crypto.utils import base64_encode, base64_decode
from mkm import SymmetricKey, ID

from dkd import Content, Message
from dkd import InstantMessage, SecureMessage, ReliableMessage
from dkd import InstantMessageDelegate, ReliableMessageDelegate

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

    # --------

    def __is_broadcast_message(self, msg: Message) -> bool:
        if isinstance(msg, InstantMessage):
            receiver = msg.content.group
        else:
            receiver = msg.envelope.group
        if receiver is None:
            receiver = msg.envelope.receiver
        identifier = self.barrack.identifier(receiver)
        return identifier.is_broadcast

    def __password(self, sender: ID, receiver: ID) -> Optional[SymmetricKey]:
        key_cache = self.key_cache
        # 1. get old key from store
        old_key = key_cache.cipher_key(sender=sender, receiver=receiver)
        # 2. get new key from delegate
        new_key = key_cache.reuse_cipher_key(key=old_key, sender=sender, receiver=receiver)
        if new_key is None:
            if old_key is None:
                # 3. create a new key
                new_key = SymmetricKey(key={'algorithm': SymmetricKey.AES})
            else:
                new_key = old_key
        # 4. update new key into the key store
        if new_key != old_key:
            key_cache.cache_cipher_key(key=new_key, sender=sender, receiver=receiver)
        return new_key

    #
    #  Transform
    #
    def encrypt_message(self, msg: InstantMessage) -> SecureMessage:
        barrack = self.barrack
        sender = barrack.identifier(msg.envelope.sender)
        receiver = barrack.identifier(msg.envelope.receiver)
        # if 'group' exists and the 'receiver' is a group ID,
        # they must be equal
        group = barrack.identifier(msg.content.group)
        # 1. get symmetric key
        if group is None:
            password = self.__password(sender=sender, receiver=receiver)
        else:
            # group message
            password = self.__password(sender=sender, receiver=group)
        assert isinstance(password, dict), 'password error: %s' % password
        # check message delegate
        if msg.delegate is None:
            msg.delegate = self
        assert msg.content is not None, 'message content empty: %s' % msg
        # 2. encrypt 'content' to 'data' for receiver/group members
        if receiver.type.is_group():
            # group message
            grp = barrack.group(identifier=receiver)
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
        # sign 'data' by sender
        return msg.sign()

    def verify_message(self, msg: ReliableMessage) -> Optional[SecureMessage]:
        #
        # TODO: check [Meta Protocol]
        #       make sure the sender's meta exists
        #       (do in by application)
        #
        if msg.delegate is None:
            msg.delegate = self
        assert msg.signature is not None, 'message signature empty: %s' % msg
        # verify 'data' with 'signature'
        return msg.verify()

    def decrypt_message(self, msg: SecureMessage) -> Optional[InstantMessage]:
        #
        # NOTICE: make sure the receiver is YOU!
        #         which means the receiver's private key exists;
        #         if the receiver is a group ID, split it first
        #
        if msg.delegate is None:
            msg.delegate = self
        assert msg.data is not None, 'message data empty: %s' % msg
        # decrypt 'data' to 'content'
        return msg.decrypt()
        # TODO: check top-secret message
        #       (do it by application)

    #
    #  De/serialize message content, symmetric key, reliable message
    #
    def serialize_content(self, content: Content, msg: InstantMessage) -> bytes:
        assert self.barrack.identifier(msg.envelope.receiver).valid, 'receiver ID error: %s' % msg
        assert content == msg.content, 'content not match: %s, %s' % (content, msg)
        string = json.dumps(content)
        return string.encode('utf-8')

    def serialize_key(self, key: SymmetricKey, msg: InstantMessage) -> bytes:
        assert not self.__is_broadcast_message(msg=msg), 'broadcast message has no key: %s' % msg
        string = json.dumps(key)
        return string.encode('utf-8')

    def serialize_message(self, msg: ReliableMessage) -> bytes:
        assert self.barrack.identifier(msg.envelope.receiver).valid, 'receiver ID error: %s' % msg
        string = json.dumps(msg)
        return string.encode('utf-8')

    def deserialize_message(self, data: bytes) -> Optional[ReliableMessage]:
        assert self
        string = data.decode('utf-8')
        dictionary = json.loads(string)
        # TODO: translate short keys
        #       'S' -> 'sender'
        #       'R' -> 'receiver'
        #       'W' -> 'time'
        #       'T' -> 'type'
        #       'G' -> 'group'
        #       ------------------
        #       'D' -> 'data'
        #       'V' -> 'signature'
        #       'K' -> 'key'
        #       ------------------
        #       'M' -> 'meta'
        return ReliableMessage(dictionary)

    def deserialize_key(self, key: bytes, msg: SecureMessage) -> Optional[SymmetricKey]:
        assert not self.__is_broadcast_message(msg=msg), 'broadcast message has no key: %s' % msg
        string = key.decode('utf-8')
        dictionary = json.loads(string)
        # TODO: translate short keys
        #       'A' -> 'algorithm'
        #       'D' -> 'data'
        #       'V' -> 'iv'
        #       'M' -> 'mode'
        #       'P' -> 'padding'
        return SymmetricKey(key=dictionary)

    def deserialize_content(self, data: bytes, msg: SecureMessage) -> Optional[Content]:
        assert self.barrack.identifier(msg.envelope.sender).valid, 'sender ID error: %s' % msg
        string = data.decode('utf-8')
        dictionary = json.loads(string)
        # TODO: translate short keys
        #       'T' -> 'type'
        #       'N' -> 'sn'
        #       'G' -> 'group'
        return Content(dictionary)

    #
    #   InstantMessageDelegate
    #
    def encrypt_content(self, content: Content, key: dict, msg: InstantMessage) -> bytes:
        # NOTICE: check attachment for File/Image/Audio/Video message content
        #         before serialize content, this job should be do in subclass
        password = SymmetricKey(key=key)
        assert password == key, 'irregular symmetric key: %s' % key
        data = self.serialize_content(content=content, msg=msg)
        return password.encrypt(data=data)

    def encode_data(self, data: bytes, msg: InstantMessage) -> str:
        if self.__is_broadcast_message(msg=msg):
            # broadcast message content will not be encrypted (just encoded to JsON),
            # so no need to encode to Base64 here
            return data.decode('utf-8')
        return base64_encode(data)

    def encrypt_key(self, key: dict, receiver: str, msg: InstantMessage) -> Optional[bytes]:
        if self.__is_broadcast_message(msg=msg):
            # broadcast message has no key
            return None
        password = SymmetricKey(key=key)
        assert password == key, 'irregular symmetric key: %s' % key
        # TODO: check whether support reused key

        data = self.serialize_key(key=password, msg=msg)
        # encrypt with receiver's public key
        barrack = self.barrack
        contact = barrack.user(identifier=barrack.identifier(receiver))
        assert contact is not None, 'failed to encrypt for receiver: %s' % receiver
        return contact.encrypt(data=data)

    def encode_key(self, key: bytes, msg: InstantMessage) -> Optional[str]:
        assert not self.__is_broadcast_message(msg=msg), 'broadcast message has no key'
        # encode to Base64
        return base64_encode(key)

    #
    #   SecureMessageDelegate
    #
    def decode_key(self, key: str, msg: SecureMessage) -> Optional[bytes]:
        assert not self.__is_broadcast_message(msg=msg), 'broadcast message has no key'
        # decode from Base64
        return base64_decode(key)

    def decrypt_key(self, key: bytes, sender: str, receiver: str, msg: SecureMessage) -> Optional[dict]:
        assert not self.__is_broadcast_message(msg=msg) or key is None, 'broadcast message has no key'
        barrack = self.barrack
        key_cache = self.key_cache
        sender = barrack.identifier(sender)
        receiver = barrack.identifier(receiver)
        if key is None:
            # if key data is empty, get it from key store
            password = key_cache.cipher_key(sender=sender, receiver=receiver)
        else:
            # decrypt key data with the receiver's private key
            identifier = barrack.identifier(msg.envelope.receiver)
            user = barrack.user(identifier=identifier)
            assert user is not None, 'failed to create local user: %s' % identifier
            plaintext = user.decrypt(data=key)
            if plaintext is None:
                raise AssertionError('failed to decrypt key in msg: %s' % msg)
            # deserialize it to symmetric key
            password = self.deserialize_key(key=plaintext, msg=msg)
            # cache the new key in key store
            key_cache.cache_cipher_key(key=password, sender=sender, receiver=receiver)
        assert isinstance(password, dict), 'failed to decrypt key: %s -> %s' % (sender, receiver)
        return password

    def decode_data(self, data: str, msg: SecureMessage) -> Optional[bytes]:
        if self.__is_broadcast_message(msg=msg):
            # broadcast message content will not be encrypted (just encoded to JsON),
            # so return the string data directly
            return data.encode('utf-8')
        return base64_decode(data)

    def decrypt_content(self, data: bytes, key: dict, msg: SecureMessage) -> Optional[Content]:
        password = SymmetricKey(key=key)
        if password is None:
            # irregular symmetric key
            return None
        plaintext = password.decrypt(data)
        if plaintext is None:
            # raise ValueError('failed to decrypt data: %s, password: %s' % (data, password))
            return None
        # NOTICE: check attachment for File/Image/Audio/Video message content
        #         after deserialize content, this job should be do in subclass
        return self.deserialize_content(data=plaintext, msg=msg)

    def sign_data(self, data: bytes, sender: str, msg: SecureMessage) -> bytes:
        barrack = self.barrack
        sender = barrack.identifier(sender)
        user = barrack.user(identifier=sender)
        assert user is not None, 'failed to sign with sender: %s' % sender
        return user.sign(data)

    def encode_signature(self, signature: bytes, msg: SecureMessage) -> str:
        return base64_encode(signature)

    #
    #   ReliableMessageDelegate
    #
    def decode_signature(self, signature: str, msg: ReliableMessage) -> Optional[bytes]:
        return base64_decode(signature)

    def verify_data_signature(self, data: bytes, signature: bytes, sender: str, msg: ReliableMessage) -> bool:
        barrack = self.barrack
        sender = barrack.identifier(sender)
        contact = barrack.user(identifier=sender)
        assert contact is not None, 'failed to verify signature for sender: %s' % sender
        return contact.verify(data=data, signature=signature)
