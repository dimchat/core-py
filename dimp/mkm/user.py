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

from abc import ABC, abstractmethod
from typing import Optional, List

from mkm.crypto import EncryptKey, DecryptKey, SignKey, VerifyKey
from mkm import ID, Visa

from .entity import EntityDataSource, Entity


class UserDataSource(EntityDataSource, ABC):
    """ This interface is for getting information for user

        User Data Source
        ~~~~~~~~~~~~~~~~

        (Encryption/decryption)
        1. public key for encryption
           if visa.key not exists, means it is the same key with meta.key
        2. private keys for decryption
           the private keys paired with [visa.key, meta.key]

        (Signature/Verification)
        3. private key for signature
           the private key paired with visa.key or meta.key
        4. public keys for verification
           [visa.key, meta.key]

        (Visa Document)
        5. private key for visa signature
           the private key pared with meta.key
        6. public key for visa verification
           meta.key only
    """

    @abstractmethod
    def contacts(self, identifier: ID) -> List[ID]:
        """
        Get user's contacts list

        :param identifier: user ID
        :return: contact ID list
        """
        pass

    @abstractmethod
    def public_key_for_encryption(self, identifier: ID) -> Optional[EncryptKey]:
        """
        Get user's public key for encryption
        (visa.key or meta.key)

        :param identifier: user ID
        :return: public key
        """
        pass

    @abstractmethod
    def public_keys_for_verification(self, identifier: ID) -> List[VerifyKey]:
        """
        Get user's public keys for verification
        [visa.key, meta.key]

        :param identifier: user ID
        :return: public keys
        """
        pass

    @abstractmethod
    def private_keys_for_decryption(self, identifier: ID) -> List[DecryptKey]:
        """
        Get user's private keys for decryption
        (which paired with [visa.key, meta.key])

        :param identifier: user ID
        :return: private keys
        """
        raise NotImplemented

    @abstractmethod
    def private_key_for_signature(self, identifier: ID) -> Optional[SignKey]:
        """
        Get user's private key for signature
        (which paired with visa.key or meta.key)

        :param identifier: user ID
        :return: private key
        """
        raise NotImplemented

    @abstractmethod
    def private_key_for_visa_signature(self, identifier: ID) -> Optional[SignKey]:
        """
        Get user's private key for signing visa

        :param identifier: user ID
        :return: private key
        """
        raise NotImplemented


class User(Entity, ABC):
    """ This class is for creating user

        User for communication
        ~~~~~~~~~~~~~~~~~~~~~~

        functions:
            (User)
            1. verify(data, signature) - verify (encrypted content) data and signature
            2. encrypt(data)           - encrypt (symmetric key) data
            (LocalUser)
            3. sign(data)    - calculate signature of (encrypted content) data
            4. decrypt(data) - decrypt (symmetric key) data
    """

    @property
    def data_source(self) -> Optional[UserDataSource]:
        raise NotImplemented

    @data_source.setter
    def data_source(self, delegate: UserDataSource):
        raise NotImplemented

    @property
    def visa(self) -> Optional[Visa]:
        raise NotImplemented

    @property
    def contacts(self) -> List[ID]:
        """
        Get all contacts of the user

        :return: contacts list
        """
        raise NotImplemented

    def verify(self, data: bytes, signature: bytes) -> bool:
        """
        Verify data and signature with user's public keys

        :param data:
        :param signature:
        :return:
        """
        raise NotImplemented

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data, try visa.key first, if not found, use meta.key

        :param data: plaintext
        :return: encrypted data
        """
        raise NotImplemented

    #
    #   interfaces for local user
    #
    def sign(self, data: bytes) -> bytes:
        """
        Sign data with user's private key

        :param data: message data
        :return: signature
        """
        raise NotImplemented

    def decrypt(self, data: bytes) -> Optional[bytes]:
        """
        Decrypt data with user's private key(s)

        :param data: encrypted data
        :return: plaintext
        """
        raise NotImplemented

    #
    #   Interfaces for Visa
    #
    def sign_visa(self, visa: Visa) -> Visa:
        # NOTICE: only sign visa with the private key paired with your meta.key
        raise NotImplemented

    def verify_visa(self, visa: Visa) -> bool:
        # NOTICE: only verify visa with meta.key
        #         (if meta not exists, user won't be created)
        raise NotImplemented
