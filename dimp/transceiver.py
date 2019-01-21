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

from dkd import SymmetricKey, PrivateKey, PublicKey
from dkd import ID, Account, Group
from dkd import InstantMessage, SecureMessage, ReliableMessage


class KeyStore:

    # @abstractmethod
    def symmetric_key(self, sender: ID=None, receiver: ID=None) -> SymmetricKey:
        """
        Get password for/from remote account.
        1. when received a message (sender was set),
           it's for decrypting secure message from sender
        2. when sending out a message (receiver was set),
           it's for encrypting instant message to receiver

        :param sender:   Received message's sender
        :param receiver: Sending out message's receiver
        :return: SymmetricKey object
        """
        pass

    # @abstractmethod
    def save_symmetric_key(self, password: SymmetricKey, sender: ID=None, receiver: ID=None):
        """
        Save password for/from remote account.

        :param password: SymmetricKey object
        :param sender:   Received message's sender
        :param receiver: Sending out message's receiver
        """
        pass


class Barrack:

    # @abstractmethod
    def account(self, identifier: ID) -> Account:
        """
        Get account

        :param identifier: Account's ID
        :return: Account object
        """
        pass

    # @abstractmethod
    def group(self, identifier: ID) -> Group:
        """
        Get group

        :param identifier: Group's ID
        :return: Group object
        """
        pass

    def public_key(self, identifier: ID) -> PublicKey:
        """
        Get public key for verifying reliable message, or encrypting password

        :param identifier: Received message's sender, or sending out message's receiver
        :return: PublicKey object
        """
        account = self.account(identifier=identifier)
        if account:
            return account.publicKey
        else:
            raise LookupError('Account not found: ' + identifier)

    # @abstractmethod
    def public_keys(self, identifier: ID) -> dict:
        """
        Get public keys for encrypting password (Group message)

        :param identifier: Sending out message's sender
        :return: A List of PublicKey objects
        """
        group = self.group(identifier=identifier)
        if group:
            keys = {}
            for member in group.members:
                keys[member] = self.public_key(identifier=member)
            return keys
        else:
            raise LookupError('Group not found: ' + identifier)


class Transceiver:

    def __init__(self, account: Account, private_key: PrivateKey,
                 barrack: Barrack, store: KeyStore):
        """

        :param account: Current account
        :param barrack: Factory for getting accounts
        :param store: Database for getting keys
        """
        super().__init__()
        self.account = account
        self.private_key = private_key
        self.barrack = barrack
        self.store = store

    def encrypt(self, msg: InstantMessage) -> SecureMessage:
        receiver = msg.envelope.receiver
        password = self.store.symmetric_key(receiver=receiver)
        if receiver.address.network.is_communicator():
            # encrypt personal message
            public_key = self.barrack.public_key(identifier=receiver)
            return msg.encrypt(password=password, public_key=public_key)
        elif receiver.address.network.is_group():
            # encrypt group message
            public_keys = self.barrack.public_keys(identifier=receiver)
            return msg.encrypt(password=password, public_keys=public_keys)
        else:
            raise ValueError('Receiver error: ' + receiver)

    def decrypt(self, msg: SecureMessage) -> InstantMessage:
        sender = msg.envelope.sender
        receiver = msg.envelope.receiver
        # trim message
        if receiver.address.network.is_group():
            group = self.barrack.group(receiver)
            msg = msg.trim(member=self.account.identifier, group=group)
        else:
            msg = msg.trim(member=self.account.identifier)

        password = self.store.symmetric_key(sender=sender)
        private_key = self.private_key
        return msg.decrypt(password=password, private_key=private_key)

    def sign(self, msg: SecureMessage) -> ReliableMessage:
        private_key = self.private_key
        return msg.sign(private_key=private_key)

    def verify(self, msg: ReliableMessage) -> SecureMessage:
        sender = msg.envelope.sender
        account = self.barrack.account(identifier=sender)
        if account:
            return msg.verify(public_key=account.publicKey)
        else:
            raise LookupError('Sender not found: ' + sender)
