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
    Delegates
    ~~~~~~~~~

    Delegates for Transceiver, such as Barrack, KeyStore, Callbacks, ...
"""

from abc import ABCMeta, abstractmethod

from dkd import InstantMessage
from mkm import SymmetricKey, ID, Account, User, Group, IEntityDataSource


class ISocialNetworkDataSource(IEntityDataSource):

    @abstractmethod
    def identifier(self, string: str) -> ID:
        """
        Create entity ID with String

        :param string: ID string
        :return: ID object
        """
        pass

    @abstractmethod
    def account(self, identifier: ID) -> Account:
        """
        Create account with ID

        :param identifier: ID object
        :return: Account object
        """
        pass

    @abstractmethod
    def user(self, identifier: ID) -> User:
        """
        Create user with ID

        :param identifier: ID object
        :return: User object
        """
        pass

    @abstractmethod
    def group(self, identifier: ID) -> Group:
        """
        Create group with ID

        :param identifier: ID object
        :return: Group object
        """
        pass


class ICipherKeyDataSource(metaclass=ABCMeta):

    @abstractmethod
    def cipher_key(self, sender: ID, receiver: ID) -> SymmetricKey:
        """
        Get cipher key for encrypt message from 'sender' to 'receiver'

        :param sender:   user or contact ID
        :param receiver: contact or user/group ID
        :return:         cipher key
        """
        pass

    @abstractmethod
    def cache_cipher_key(self, key: SymmetricKey, sender: ID, receiver: ID):
        """
        Cache cipher key for reusing, with direction (from 'sender' to 'receiver')

        :param key:      cipher key from a contact
        :param sender:   user or contact ID
        :param receiver: contact or user/group ID
        """
        pass

    @abstractmethod
    def reuse_cipher_key(self, key: SymmetricKey, sender: ID, receiver: ID) -> SymmetricKey:
        """
        Update/create cipher key for encrypt message content

        :param sender:   user ID
        :param receiver: contact/group ID
        :param key:      old key to be reused (nullable)
        :return:         new key
        """
        pass


class ICallback(metaclass=ABCMeta):

    @abstractmethod
    def finished(self, result, error):
        pass


class ICompletionHandler(metaclass=ABCMeta):

    @abstractmethod
    def success(self):
        pass

    @abstractmethod
    def failed(self, error):
        pass


class ITransceiverDelegate(metaclass=ABCMeta):

    @abstractmethod
    def send_package(self, data: bytes, handler: ICompletionHandler) -> bool:
        """
        Send out a data package onto network

        :param data:    package data
        :param handler: completion handler
        :return:        False on data/delegate error
        """
        pass

    @abstractmethod
    def upload_data(self, data: bytes, msg: InstantMessage) -> str:
        """
        Upload encrypted data to CDN

        :param data: encrypted file data
        :param msg:  instant message
        :return:     download URL
        """
        pass

    @abstractmethod
    def download_data(self, url: str, msg: InstantMessage) -> bytes:
        """
        Download encrypted data from CDN, and decrypt it when finished

        :param url: download URL
        :param msg: instant message
        :return:    encrypted file data
        """
        pass
