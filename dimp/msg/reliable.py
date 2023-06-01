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

from typing import Optional, Any, Dict

from mkm import Meta, Document, Visa

from dkd import SecureMessage, ReliableMessage
from dkd import ReliableMessageFactory, ReliableMessageDelegate

from .secure import EncryptedMessage


"""
    Network Message
    ~~~~~~~~~~~~~~~

    Implementations for ReliableMessage
"""


class NetworkMessage(EncryptedMessage, ReliableMessage):

    def __init__(self, msg: Dict[str, Any]):
        super().__init__(msg=msg)
        # lazy
        self.__signature = None
        self.__meta = None
        self.__visa = None

    @property  # Override
    def signature(self) -> bytes:
        if self.__signature is None:
            base64 = self.get(key='signature')
            # assert base64 is not None, 'signature of reliable message cannot be empty: %s' % self
            delegate = self.delegate
            assert isinstance(delegate, ReliableMessageDelegate), 'reliable delegate error: %s' % delegate
            self.__signature = delegate.decode_signature(signature=base64, msg=self)
        return self.__signature

    @property  # Override
    def meta(self) -> Optional[Meta]:
        if self.__meta is None:
            info = self.get(key='meta')
            self.__meta = Meta.parse(meta=info)
        return self.__meta

    @meta.setter  # Override
    def meta(self, info: Meta):
        if info is None:
            self.pop('meta', None)
        else:
            self['meta'] = info.dictionary
        self.__meta = info

    @property  # Override
    def visa(self) -> Optional[Visa]:
        if self.__visa is None:
            info = self.get(key='visa')
            self.__visa = Document.parse(document=info)
        return self.__visa

    @visa.setter  # Override
    def visa(self, info: Visa):
        if info is None:
            self.pop('visa', None)
        else:
            self['visa'] = info.dictionary
        self.__visa = info

    # Override
    def verify(self) -> Optional[SecureMessage]:
        data = self.data
        if data is None:
            raise ValueError('failed to decode content data: %s' % self)
        signature = self.signature
        if signature is None:
            raise ValueError('failed to decode message signature: %s' % self)
        # 1. verify data signature
        delegate = self.delegate
        assert isinstance(delegate, ReliableMessageDelegate), 'reliable delegate error: %s' % delegate
        if delegate.verify_data_signature(data=data, signature=signature, sender=self.sender, msg=self):
            # 2. pack message
            msg = self.copy_dictionary()
            msg.pop('signature')  # remove 'signature'
            return SecureMessage.parse(msg=msg)
        # else:
        #     # TODO: check whether visa is expired, query new document for this contact
        #     raise ValueError('Signature error: %s' % self)


class NetworkMessageFactory(ReliableMessageFactory):

    # Override
    def parse_reliable_message(self, msg: Dict[str, Any]) -> Optional[ReliableMessage]:
        # check 'sender', 'data', 'signature'
        sender = msg.get('sender')
        data = msg.get('data')
        signature = msg.get('signature')
        if sender is None or data is None or signature is None:
            # msg.sender should not be empty
            # msg.data should not be empty
            # msg.signature should not be empty
            return None
        return NetworkMessage(msg=msg)
