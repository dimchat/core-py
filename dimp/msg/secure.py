# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
#
#                                Written in 2021 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2021 Albert Moky
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

from typing import Optional, Any, Dict, List

from mkm import ID

from dkd import InstantMessage, SecureMessage, ReliableMessage
from dkd import SecureMessageFactory, SecureMessageDelegate

from .base import BaseMessage


"""
    Encrypted Message
    ~~~~~~~~~~~~~~~~~

    Implementations for SecureMessage
"""


class EncryptedMessage(BaseMessage, SecureMessage):

    def __init__(self, msg: Dict[str, Any]):
        super().__init__(msg=msg)
        # lazy
        self.__data = None
        self.__key = None
        self.__keys = None

    @property  # Override
    def data(self) -> bytes:
        if self.__data is None:
            base64 = self.get(key='data')
            # assert base64 is not None, 'secure message data cannot be empty: %s' % self
            delegate = self.delegate
            assert isinstance(delegate, SecureMessageDelegate), 'secure delegate error: %s' % delegate
            self.__data = delegate.decode_data(data=base64, msg=self)
        return self.__data

    @property  # Override
    def encrypted_key(self) -> Optional[bytes]:
        if self.__key is None:
            base64 = self.get(key='key')
            if base64 is None:
                # check 'keys'
                keys = self.encrypted_keys
                if keys is not None:
                    receiver = str(self.receiver)
                    base64 = keys.get(receiver)
            if base64 is not None:
                delegate = self.delegate
                assert isinstance(delegate, SecureMessageDelegate), 'secure delegate error: %s' % delegate
                self.__key = delegate.decode_key(key=base64, msg=self)
        return self.__key

    @property  # Override
    def encrypted_keys(self) -> Optional[Dict[str, Any]]:
        if self.__keys is None:
            self.__keys = self.get(key='keys')
        return self.__keys

    # Override
    def decrypt(self) -> Optional[InstantMessage]:
        sender = self.sender
        group = self.group
        if group is None:
            # personal message
            # not split group message
            receiver = self.receiver
        else:
            # group message
            receiver = group

        # 1. decrypt 'message.key' to symmetric key
        delegate = self.delegate
        assert isinstance(delegate, SecureMessageDelegate), 'secure delegate error: %s' % delegate
        # 1.1. decode encrypted key data
        key = self.encrypted_key
        # 1.2. decrypt key data
        if key is not None:
            key = delegate.decrypt_key(data=key, sender=sender, receiver=receiver, msg=self)
            if key is None:
                raise AssertionError('failed to decrypt key in msg: %s' % self)
        # 1.3. deserialize key
        #      if key is empty, means it should be reused, get it from key cache
        password = delegate.deserialize_key(data=key, sender=sender, receiver=receiver, msg=self)
        if password is None:
            raise ValueError('failed to get msg key: %s -> %s, %s' % (sender, receiver, key))

        # 2. decrypt 'message.data' to 'message.content'
        # 2.1. decode encrypted content data
        data = self.data
        if data is None:
            raise ValueError('failed to decode content data: %s' % self)
        # 2.2. decrypt content data
        plaintext = delegate.decrypt_content(data=data, key=password, msg=self)
        if plaintext is None:
            raise ValueError('failed to decrypt data with key: %s, %s' % (password, data))
        # 2.3. deserialize content
        content = delegate.deserialize_content(data=plaintext, key=password, msg=self)
        if content is None:
            raise ValueError('failed to deserialize content: %s' % plaintext)
        # 2.4. check attachment for File/Image/Audio/Video message content
        #      if file data not download yet,
        #          decrypt file data with password;
        #      else,
        #          save password to 'message.content.password'.
        #      (do it in 'core' module)

        # 3. pack message
        msg = self.copy_dictionary()
        msg.pop('key', None)
        msg.pop('keys', None)
        msg.pop('data')
        msg['content'] = content.dictionary
        return InstantMessage.parse(msg=msg)

    # Override
    def sign(self) -> ReliableMessage:
        data = self.data
        delegate = self.delegate
        assert isinstance(delegate, SecureMessageDelegate), 'secure delegate error: %s' % delegate
        # 1. sign message.data
        signature = delegate.sign_data(data=data, sender=self.sender, msg=self)
        assert signature is not None, 'failed to sign message: %s' % self
        # 2. encode signature
        base64 = delegate.encode_signature(signature=signature, msg=self)
        assert base64 is not None, 'failed to encode signature: %s' % signature
        # 3. pack message
        msg = self.copy_dictionary()
        msg['signature'] = base64
        return ReliableMessage.parse(msg=msg)

    # Override
    def split(self, members: List[ID]) -> List[SecureMessage]:
        msg = self.copy_dictionary()
        # check 'keys'
        keys = msg.get('keys')
        if keys is None:
            keys = {}
        else:
            msg.pop('keys')

        # 1. move the receiver(group ID) to 'group'
        #    this will help the receiver knows the group ID
        #    when the group message separated to multi-messages;
        #    if don't want the others know your membership,
        #    DON'T do this.
        msg['group'] = str(self.receiver)

        messages = []
        for member in members:
            receiver = str(member)
            # 2. change 'receiver' to each group member
            msg['receiver'] = receiver
            # 3. get encrypted key
            key = keys.get(receiver)
            if key is None:
                msg.pop('key', None)
            else:
                msg['key'] = key
            # 4. pack message
            item = SecureMessage.parse(msg=msg.copy())
            if item is not None:
                messages.append(item)
        # OK
        return messages

    # Override
    def trim(self, member: ID) -> SecureMessage:
        msg = self.copy_dictionary()
        receiver = str(member)
        # check keys
        keys = msg.get('keys')
        if keys is not None:
            # move key data from 'keys' to 'key'
            key = keys.get(receiver)
            if key is not None:
                msg['key'] = key
            msg.pop('keys')
        # check 'group'
        group = self.group
        if group is None:
            assert self.receiver.is_group, 'receiver is not a group ID: %s' % self.receiver
            # if 'group' not exists, the 'receiver' must be a group ID here, and
            # it will not be equal to the member of course,
            # so move 'receiver' to 'group'
            msg['group'] = str(self.receiver)
        # replace receiver
        msg['receiver'] = receiver
        return SecureMessage.parse(msg=msg)


class EncryptedMessageFactory(SecureMessageFactory):

    # Override
    def parse_secure_message(self, msg: Dict[str, Any]) -> Optional[SecureMessage]:
        # check 'sender', 'data'
        sender = msg.get('sender')
        data = msg.get('data')
        if sender is None or data is None:
            # msg.sender should not be empty
            # msg.data should not be empty
            return None
        # check 'signature'
        signature = msg.get('signature')
        if signature is not None:
            from .reliable import NetworkMessage
            return NetworkMessage(msg=msg)
        return EncryptedMessage(msg=msg)
