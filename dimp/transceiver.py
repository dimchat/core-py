# -*- coding: utf-8 -*-
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

from dkd import MessageType, Content, ForwardContent
from dkd import InstantMessage, SecureMessage, ReliableMessage
from dkd import IInstantMessageDelegate, ISecureMessageDelegate, IReliableMessageDelegate

from mkm import SymmetricKey, PrivateKey
from mkm import Meta, ID

from .keystore import KeyStore
from .barrack import Barrack


class Transceiver(IInstantMessageDelegate, ISecureMessageDelegate, IReliableMessageDelegate):

    def __init__(self, identifier: ID, private_key: PrivateKey, barrack: Barrack, key_store: KeyStore):
        """

        :param identifier:  Current account's ID
        :param private_key: Current account's private key
        :param barrack:     Factory for getting accounts
        :param key_store:   Database for getting symmetric keys
        """
        super().__init__()
        self.identifier = identifier
        self.private_key = private_key
        # databases
        self.barrack = barrack
        self.key_store = key_store

    #
    #   IInstantMessageDelegate
    #
    def message_encrypt_key(self, msg: InstantMessage, key: dict, receiver: str) -> bytes:
        contact = self.barrack.account_create(identifier=ID(receiver))
        pk = contact.publicKey
        string = json.dumps(key)
        return pk.encrypt(plaintext=string.encode('utf-8'))

    def message_encrypt_content(self, msg: InstantMessage, content: Content, key: dict) -> bytes:
        password = SymmetricKey(key)
        string = json.dumps(content)
        return password.encrypt(plaintext=string.encode('utf-8'))

    #
    #   ISecureMessageDelegate
    #
    def message_decrypt_key(self, msg: SecureMessage, key: bytes, sender: str, receiver: str, group: str=None) -> dict:
        sender = ID(sender)
        receiver = ID(receiver)
        if group:
            group = ID(group)
        if key is None:
            # the message contains no key, try reuse a key from local cache
            if group:
                return self.key_store.cipher_key(sender=sender, receiver=group)
            else:
                return self.key_store.cipher_key(sender=sender, receiver=receiver)
        # decrypt it with receiver's private key
        if receiver == self.identifier:
            sk = self.private_key
        else:
            # get private key from database
            sk = self.barrack.private_key(identifier=receiver)
        if sk is None:
            raise LookupError('failed to get private key for %s' % receiver)
        data = sk.decrypt(data=key)
        if data is None:
            raise ValueError('failed to decrypt symmetric key: %s for %s' % (key, receiver))
        dictionary = json.loads(data)
        pwd = SymmetricKey(dictionary)
        # save the new key into local cache for reuse
        if group:
            self.key_store.cache_cipher_key(key=pwd, sender=sender, receiver=group)
        else:
            self.key_store.cache_cipher_key(key=pwd, sender=sender, receiver=receiver)
        return pwd

    def message_decrypt_content(self, msg: SecureMessage, data: bytes, key: dict) -> Content:
        pwd = SymmetricKey(key)
        plaintext = pwd.decrypt(data)
        dictionary = json.loads(plaintext)
        return Content(dictionary)

    def message_sign(self, msg: SecureMessage, data: bytes, sender: str) -> bytes:
        identifier = ID(sender)
        if identifier == self.identifier:
            sk = self.private_key
        else:
            # get private key from database
            sk = self.barrack.private_key(identifier=identifier)
        return sk.sign(data)

    #
    #   IReliableMessageDelegate
    #
    def message_verify(self, msg: ReliableMessage, data: bytes, signature: bytes, sender: str) -> bool:
        contact = self.barrack.account_create(identifier=ID(sender))
        pk = contact.publicKey
        return pk.verify(data=data, signature=signature)

    #
    #   Conveniences
    #
    def encrypt_sign(self, msg: InstantMessage) -> ReliableMessage:
        sender = ID(msg.envelope.sender)
        receiver = ID(msg.envelope.receiver)
        group = msg.content.group
        if group:
            group = ID(group)
        elif receiver.type.is_group():
            group = receiver
        # 1. encrypt 'content' to 'data' for receiver
        if msg.delegate is None:
            msg.delegate = self
        if group:
            # group message
            grp = self.barrack.group_create(identifier=group)
            key = self.key_store.cipher_key(sender=sender, receiver=group)
            s_msg = msg.encrypt(password=key, members=grp.members)
        else:
            # personal message
            key = self.key_store.cipher_key(sender=sender, receiver=receiver)
            s_msg = msg.encrypt(password=key)
        # 2. sign
        s_msg.delegate = self
        return s_msg.sign()

    def verify_decrypt(self, msg: ReliableMessage) -> InstantMessage:
        sender = ID(msg.envelope.sender)
        receiver = ID(msg.envelope.receiver)
        # [Meta Protocol] check meta in first contact message
        meta = self.barrack.meta(identifier=sender)
        if meta is None:
            # first contact, try meta in message package
            meta = msg.meta
            if meta is None:
                # TODO: query meta for sender from DIM network
                raise LookupError('failed to get meta for sender: %s' % sender)
            meta = Meta(meta)
            if meta.match_identifier(identifier=sender):
                self.barrack.cache_meta(meta=meta, identifier=sender)
            else:
                raise ValueError('meta not match %s, %s' % (sender, meta))
        # 1. verify 'data' with 'signature'
        if msg.delegate is None:
            msg.delegate = self
        s_msg = msg.verify()
        # check recipient
        if receiver.type.is_group():
            group = receiver
            # FIXME: maybe other user?
            receiver = self.identifier
        else:
            group = msg.group
            if group is not None:
                group = ID(group)
        # 2. decrypt 'data' to 'content'
        if group is not None:
            # trim for user(group member)
            s_msg = s_msg.trim(member=receiver)
            s_msg.delegate = self
            i_msg = s_msg.decrypt(member=receiver)
        else:
            # personal message
            s_msg.delegate = self
            i_msg = s_msg.decrypt()
        # 3. check: top-secret message
        if i_msg.content.type == MessageType.Forward:
            content = ForwardContent(i_msg.content)
            return self.verify_decrypt(content.forward)
        # OK
        return i_msg
