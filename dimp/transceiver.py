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

from mkm import Base64
from mkm import SymmetricKey, ID

from dkd import Content, Message
from dkd import InstantMessage, SecureMessage, ReliableMessage
from dkd import InstantMessageDelegate, ReliableMessageDelegate

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
        # get old key from cache
        key = key_cache.cipher_key(sender=sender, receiver=receiver)
        if key is None:
            # create new key and cache it
            key = SymmetricKey(key={'algorithm': SymmetricKey.AES})
            assert key is not None, 'failed to generate AES key'
            key_cache.cache_cipher_key(key=key, sender=sender, receiver=receiver)
        return key

    #
    #  Transform
    #

    def __overt_group(self, content: Content) -> Optional[ID]:
        group = content.group
        if group is None:
            return None
        group = self.barrack.identifier(group)
        if group.is_broadcast:
            # broadcast message is always overt
            return group
        if isinstance(content, Command):
            # group command should be sent to each member directly, so
            # don't expose group ID
            return None
        else:
            return group

    def encrypt_message(self, msg: InstantMessage) -> Optional[SecureMessage]:
        barrack = self.barrack
        sender = barrack.identifier(msg.envelope.sender)
        receiver = barrack.identifier(msg.envelope.receiver)
        # if 'group' exists and the 'receiver' is a group ID,
        # they must be equal

        # NOTICE: while sending group message, don't split it before encrypting.
        #         this means you could set group ID into message content, but
        #         keep the "receiver" to be the group ID;
        #         after encrypted (and signed), you could split the message
        #         with group members before sending out, or just send it directly
        #         to the group assistant to let it split messages for you!
        #    BUT,
        #         if you don't want to share the symmetric key with other members,
        #         you could split it (set group ID into message content and
        #         set contact ID to the "receiver") before encrypting, this usually
        #         for sending group command to assistant robot, which should not
        #         share the symmetric key (group msg key) with other members.

        # 1. get symmetric key
        group = self.__overt_group(content=msg.content)
        if group is None:
            # personal message or (group) command
            password = self.__password(sender=sender, receiver=receiver)
        else:
            # group message (excludes group command)
            password = self.__password(sender=sender, receiver=group)
        assert isinstance(password, dict), 'password error: %s' % password

        # check message delegate
        if msg.delegate is None:
            msg.delegate = self
        assert msg.content is not None, 'message content empty: %s' % msg
        # 2. encrypt 'content' to 'data' for receiver/group members
        if receiver.is_group:
            # group message
            grp = barrack.group(identifier=receiver)
            s_msg = msg.encrypt(password=password, members=grp.members)
        else:
            # personal message (or split group message)
            assert receiver.is_user, 'unknown receiver type: %s' % receiver
            s_msg = msg.encrypt(password=password)
        if s_msg is None:
            # public key for encryption not found
            # TODO: suspend this message for waiting receiver's meta
            return None

        # overt group ID
        if group is not None and receiver != group:
            # NOTICE: this help the receiver knows the group ID
            #         when the group message separated to multi-messages,
            #         if don't want the others know you are the group members,
            #         remove it.
            s_msg.envelope.group = group

        # NOTICE: copy content type to envelope
        #         this help the intermediate nodes to recognize message type
        s_msg.envelope.type = msg.content.type

        # OK
        return s_msg

    def sign_message(self, msg: SecureMessage) -> ReliableMessage:
        if msg.delegate is None:
            msg.delegate = self
        assert msg.data is not None, 'message data empty: %s' % msg
        # sign 'data' by sender
        return msg.sign()

    def serialize_message(self, msg: ReliableMessage) -> bytes:
        string = json.dumps(msg)
        return string.encode('utf-8')

    def deserialize_message(self, data: bytes) -> Optional[ReliableMessage]:
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
    #   InstantMessageDelegate
    #
    def serialize_content(self, content: Content, key: dict, msg: InstantMessage) -> bytes:
        # NOTICE: check attachment for File/Image/Audio/Video message content
        #         before serialize content, this job should be do in subclass
        assert self.barrack.identifier(msg.envelope.receiver).valid, 'receiver ID error: %s' % msg
        assert content == msg.content, 'content not match: %s, %s' % (content, msg)
        string = json.dumps(content)
        return string.encode('utf-8')

    def encrypt_content(self, data: bytes, key: dict, msg: InstantMessage) -> bytes:
        password = SymmetricKey(key=key)
        assert password == key, 'irregular symmetric key: %s' % key
        return password.encrypt(data=data)

    def encode_data(self, data: bytes, msg: InstantMessage) -> str:
        if self.__is_broadcast_message(msg=msg):
            # broadcast message content will not be encrypted (just encoded to JsON),
            # so no need to encode to Base64 here
            return data.decode('utf-8')
        return Base64.encode(data)

    def serialize_key(self, key: dict, msg: InstantMessage) -> Optional[bytes]:
        if self.__is_broadcast_message(msg=msg):
            # broadcast message has no key
            return None
        string = json.dumps(key)
        return string.encode('utf-8')

    def encrypt_key(self, data: bytes, receiver: str, msg: InstantMessage) -> Optional[bytes]:
        assert not self.__is_broadcast_message(msg=msg), 'broadcast message has no key: %s' % msg
        # TODO: make sure the receiver's public key exists
        barrack = self.barrack
        contact = barrack.user(identifier=barrack.identifier(receiver))
        assert contact is not None, 'failed to encrypt for receiver: %s' % receiver
        # encrypt with receiver's public key
        return contact.encrypt(data=data)

    def encode_key(self, data: bytes, msg: InstantMessage) -> str:
        assert not self.__is_broadcast_message(msg=msg), 'broadcast message has no key: %s' % msg
        # encode to Base64
        return Base64.encode(data)

    #
    #   SecureMessageDelegate
    #
    def decode_key(self, string: str, msg: SecureMessage) -> Optional[bytes]:
        assert not self.__is_broadcast_message(msg=msg), 'broadcast message has no key'
        # decode from Base64
        return Base64.decode(string)

    def decrypt_key(self, data: bytes, sender: str, receiver: str, msg: SecureMessage) -> Optional[bytes]:
        assert not self.__is_broadcast_message(msg=msg), 'broadcast message has no key'
        # decrypt key data with the receiver's private key
        barrack = self.barrack
        identifier = barrack.identifier(msg.envelope.receiver)
        user = barrack.user(identifier=identifier)
        assert user is not None, 'failed to create local user: %s' % identifier
        return user.decrypt(data=data)

    def deserialize_key(self, data: Optional[bytes], sender: str, receiver: str, msg: SecureMessage) -> Optional[dict]:
        if data is None:
            # get key from cache
            barrack = self.barrack
            sender = barrack.identifier(sender)
            receiver = barrack.identifier(receiver)
            return self.key_cache.cipher_key(sender=sender, receiver=receiver)
        else:
            assert not self.__is_broadcast_message(msg=msg), 'broadcast message has no key: %s' % msg
            string = data.decode('utf-8')
            dictionary = json.loads(string)
            # TODO: translate short keys
            #       'A' -> 'algorithm'
            #       'D' -> 'data'
            #       'V' -> 'iv'
            #       'M' -> 'mode'
            #       'P' -> 'padding'
            return SymmetricKey(key=dictionary)

    def decode_data(self, data: str, msg: SecureMessage) -> Optional[bytes]:
        if self.__is_broadcast_message(msg=msg):
            # broadcast message content will not be encrypted (just encoded to JsON),
            # so return the string data directly
            return data.encode('utf-8')
        return Base64.decode(data)

    def decrypt_content(self, data: bytes, key: dict, msg: SecureMessage) -> Optional[bytes]:
        password = SymmetricKey(key=key)
        if password is None:
            raise ValueError('irregular symmetric key: %s' % key)
        return password.decrypt(data)

    def deserialize_content(self, data: bytes, key: dict, msg: SecureMessage) -> Optional[Content]:
        assert self.barrack.identifier(msg.envelope.sender).valid, 'sender ID error: %s' % msg
        string = data.decode('utf-8')
        dictionary = json.loads(string)
        # TODO: translate short keys
        #       'T' -> 'type'
        #       'N' -> 'sn'
        #       'G' -> 'group'
        content = Content(dictionary)
        assert content is not None, 'content error: %d' % len(data)
        if not self.__is_broadcast_message(msg=msg):
            password = SymmetricKey(key=key)
            assert password is key, 'irregular symmetric key: %s' % key
            # check and cache key for reuse
            barrack = self.barrack
            sender = barrack.identifier(msg.envelope.sender)
            group = self.__overt_group(content=content)
            if group is None:
                receiver = barrack.identifier(msg.envelope.receiver)
                # personal message or (group) command
                # cache key with direction (sender -> receiver)
                self.key_cache.cache_cipher_key(key=password, sender=sender, receiver=receiver)
            else:
                # group message (excludes group command)
                # cache the key with direction (sender -> group)
                self.key_cache.cache_cipher_key(key=password, sender=sender, receiver=group)
        # NOTICE: check attachment for File/Image/Audio/Video message content
        #         after deserialize content, this job should be do in subclass
        return content

    def sign_data(self, data: bytes, sender: str, msg: SecureMessage) -> bytes:
        barrack = self.barrack
        sender = barrack.identifier(sender)
        user = barrack.user(identifier=sender)
        assert user is not None, 'failed to sign with sender: %s' % sender
        return user.sign(data)

    def encode_signature(self, signature: bytes, msg: SecureMessage) -> str:
        return Base64.encode(signature)

    #
    #   ReliableMessageDelegate
    #
    def decode_signature(self, signature: str, msg: ReliableMessage) -> Optional[bytes]:
        return Base64.decode(signature)

    def verify_data_signature(self, data: bytes, signature: bytes, sender: str, msg: ReliableMessage) -> bool:
        barrack = self.barrack
        sender = barrack.identifier(sender)
        contact = barrack.user(identifier=sender)
        assert contact is not None, 'failed to verify signature for sender: %s' % sender
        return contact.verify(data=data, signature=signature)
