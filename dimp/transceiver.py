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

from dkd.transform import json_dict, json_str

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
        json = json_str(key)
        return pk.encrypt(plaintext=json.encode('utf-8'))

    def message_encrypt_content(self, msg: InstantMessage, content: Content, key: dict) -> bytes:
        password = SymmetricKey(key)
        json = json_str(content)
        return password.encrypt(plaintext=json.encode('utf-8'))

    #
    #   ISecureMessageDelegate
    #
    def message_decrypt_key(self, msg: SecureMessage,
                            key: bytes, sender: str, receiver: str, group: str = None) -> dict:
        if key is None:
            # the message contains no key, try reuse a key from local cache
            return self.key_store.cipher_key(sender=sender, group=group)
        # decrypt it with receiver's private key
        identifier = ID(receiver)
        if identifier == self.identifier:
            sk = self.private_key
        else:
            # get private key from database
            sk = self.barrack.private_key(identifier=identifier)
        data = sk.decrypt(data=key)
        dictionary = json_dict(data)
        pwd = SymmetricKey(dictionary)
        if pwd:
            # save the new key into local cache for reuse
            self.key_store.retain_cipher_key(key=pwd, sender=sender, group=group)
        return pwd

    def message_decrypt_content(self, msg: SecureMessage, data: bytes, key: dict) -> Content:
        pwd = SymmetricKey(key)
        plaintext = pwd.decrypt(data)
        dictionary = json_dict(plaintext)
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
            key = self.key_store.cipher_key(group=group)
            if key is None:
                # create a new key & save it into the Key Store
                key = SymmetricKey.generate({'algorithm': 'AES'})
                self.key_store.retain_cipher_key(key, group=group)
            grp = self.barrack.group_create(identifier=group)
            members = grp.members
            s_msg = msg.encrypt(password=key, members=members)
        else:
            # personal message
            key = self.key_store.cipher_key(receiver=receiver)
            if key is None:
                # create a new key & save it into the Key Store
                key = SymmetricKey.generate({'algorithm': 'AES'})
                self.key_store.retain_cipher_key(key, group=group)
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
                self.barrack.retain_meta(meta=meta, identifier=sender)
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
