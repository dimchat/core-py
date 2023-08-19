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
    Reliable Message signed by an asymmetric key
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This class is used to sign the SecureMessage
    It contains a 'signature' field which signed with sender's private key

    data format: {
        //-- envelope
        sender   : "moki@xxx",
        receiver : "hulk@yyy",
        time     : 123,
        //-- content data and key/keys
        data     : "...",  // base64_encode(symmetric)
        key      : "...",  // base64_encode(asymmetric)
        keys     : {
            "ID1": "key1", // base64_encode(asymmetric)
        },
        //-- signature
        signature: "..."   // base64_encode()
    }
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
            if base64 is not None:
                delegate = self.delegate
                assert isinstance(delegate, ReliableMessageDelegate), 'reliable delegate error: %s' % delegate
                self.__signature = delegate.decode_signature(signature=base64, msg=self)
                assert self.__signature is not None, 'message signature error: %s' % base64
            # else:
            #     assert False, 'signature of reliable message cannot be empty: %s' % self
        return self.__signature

    @property  # Override
    def meta(self) -> Optional[Meta]:
        if self.__meta is None:
            self.__meta = Meta.parse(meta=self.get(key='meta'))
        return self.__meta

    @meta.setter  # Override
    def meta(self, info: Meta):
        self.set_map(key='meta', dictionary=info)
        self.__meta = info

    @property  # Override
    def visa(self) -> Optional[Visa]:
        if self.__visa is None:
            doc = Document.parse(document=self.get(key='visa'))
            if isinstance(doc, Visa):
                self.__visa = doc
            # else:
            #     assert False, 'visa document error: %s' % doc
        return self.__visa

    @visa.setter  # Override
    def visa(self, info: Visa):
        self.set_map(key='visa', dictionary=info)
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
        if 'sender' in msg and 'data' in msg and 'signature' in msg:
            return NetworkMessage(msg=msg)
        # msg.sender should not be empty
        # msg.data should not be empty
        # msg.signature should not be empty
