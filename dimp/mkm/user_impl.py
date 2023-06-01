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

from typing import Optional, List

from mkm import ID, Document, Visa

from .user import User, UserDataSource
from .entity_impl import BaseEntity


class BaseUser(BaseEntity, User):

    @BaseEntity.data_source.getter  # Override
    def data_source(self) -> Optional[UserDataSource]:
        return super().data_source

    # @data_source.setter  # Override
    # def data_source(self, barrack: UserDataSource):
    #     super(BaseUser, BaseUser).data_source.__set__(self, barrack)

    @property  # Override
    def visa(self) -> Optional[Visa]:
        doc = self.document(doc_type=Document.VISA)
        if isinstance(doc, Visa):
            return doc

    @property  # Override
    def contacts(self) -> List[ID]:
        barrack = self.data_source
        # assert barrack is not None, 'user delegate not set yet'
        return barrack.contacts(identifier=self.identifier)

    # Override
    def verify(self, data: bytes, signature: bytes) -> bool:
        # NOTICE: I suggest using the private key paired with meta.key to sign message,
        #         so here should return the meta.key
        barrack = self.data_source
        # assert barrack is not None, 'user delegate not set yet'
        keys = barrack.public_keys_for_verification(identifier=self.identifier)
        # assert len(keys) > 0, 'failed to get verify keys: %s' % self.identifier
        for key in keys:
            if key.verify(data=data, signature=signature):
                # matched!
                return True
        # signature not match
        # TODO: check whether visa is expired, query new document for this contact

    # Override
    def encrypt(self, data: bytes) -> bytes:
        # NOTICE: meta.key will never changed, so use visa.key to encrypt message
        #         is the better way
        barrack = self.data_source
        # assert barrack is not None, 'user delegate not set yet'
        key = barrack.public_key_for_encryption(identifier=self.identifier)
        # assert key is not None, 'failed to get encrypt key for user: %s' % self.identifier
        return key.encrypt(data=data)

    # Override
    def sign(self, data: bytes) -> bytes:
        # NOTICE: I suggest use the private key which paired to meta.key
        #         to sign message
        barrack = self.data_source
        # assert barrack is not None, 'user delegate not set yet'
        key = barrack.private_key_for_signature(identifier=self.identifier)
        # assert key is not None, 'failed to get sign key for user: %s' % self.identifier
        return key.sign(data=data)

    # Override
    def decrypt(self, data: bytes) -> Optional[bytes]:
        # NOTICE: if you provide a public key in visa document for encryption,
        #         here you should return the private key paired with visa.key
        barrack = self.data_source
        # assert barrack is not None, 'user delegate not set yet'
        keys = barrack.private_keys_for_decryption(identifier=self.identifier)
        # assert len(keys) > 0, 'failed to get decrypt keys: %s' % self.identifier
        for key in keys:
            # try decrypting it with each private key
            plaintext = key.decrypt(data=data)
            if plaintext is not None:
                # OK!
                return plaintext
        # decryption failed
        # TODO: check whether my visa key is changed, push new visa to this contact

    # Override
    def sign_visa(self, visa: Visa) -> Optional[Visa]:
        # NOTICE: only sign visa with the private key paired with your meta.key
        assert self.identifier == visa.identifier, 'visa ID not match: %s, %s' % (self.identifier, visa)
        barrack = self.data_source
        # assert barrack is not None, 'user delegate not set yet'
        key = barrack.private_key_for_visa_signature(identifier=self.identifier)
        if key is None:
            # assert False, 'failed to get sign key for visa: %s' % self.identifier
            return None
        elif visa.sign(private_key=key) is None:
            # assert False, 'failed to sign visa: %s, %s' % (self.identifier, visa)
            return None
        else:
            return visa

    # Override
    def verify_visa(self, visa: Visa) -> bool:
        # NOTICE: only verify visa with meta.key
        #         (if meta not exists, user won't be created)
        if self.identifier != visa.identifier:
            return False
        key = self.meta.key
        # assert key is not None, 'failed to get meta key for visa: %s' % self.identifier
        return visa.verify(public_key=key)
