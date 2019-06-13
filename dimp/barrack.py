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
    User Database
    ~~~~~~~~~~~~~

    Manage meta for all entities
"""

from abc import ABCMeta

from mkm import PrivateKey
from mkm import ID, Meta, Profile
from mkm import Account, User, Group
from mkm import IEntityDataSource, IUserDataSource, IGroupDataSource


class Barrack(IUserDataSource, IGroupDataSource):

    def __init__(self):
        super().__init__()

        # delegates
        self.delegate: IBarrackDelegate = None

        self.entityDataSource: IEntityDataSource = None
        self.userDataSource: IUserDataSource = None
        self.groupDataSource: IGroupDataSource = None

        # memory caches
        self.metas = {}
        self.accounts = {}
        self.users = {}
        self.groups = {}

    def reduce_memory(self) -> int:
        """
        Call it when received 'UIApplicationDidReceiveMemoryWarningNotification',
        this will remove 50% of cached objects

        :return: reduced object count
        """
        finger = 1
        finger = self.__thanos(self.metas, finger)
        finger = self.__thanos(self.accounts, finger)
        finger = self.__thanos(self.users, finger)
        finger = self.__thanos(self.groups, finger)
        return (finger & 1) + (finger >> 1)

    @staticmethod
    def __thanos(planet: dict, finger: int) -> int:
        keys = planet.keys()
        for key in keys:
            if (++finger) & 1:
                # kill it
                planet.pop(key)
        return finger

    def cache_meta(self, meta: Meta, identifier: ID):
        if not meta.match_identifier(identifier):
            raise AssertionError('meta not match ID')
        self.metas[identifier.address] = meta

    def cache_account(self, account: Account):
        if isinstance(account, User):
            return self.cache_user(user=account)
        if account.delegate is None:
            account.delegate = self
        self.accounts[account.identifier.address] = account
        return True

    def cache_user(self, user: User):
        if user.delegate is None:
            user.delegate = self
        self.users[user.identifier.address] = user

    def cache_group(self, group: Group):
        if group.delegate is None:
            group.delegate = self
        self.groups[group.identifier.address] = group

    def account(self, identifier: ID) -> Account:
        # 1. get from account cache
        account = self.accounts.get(identifier.address)
        if account is not None:
            return account
        # 2. get from user cache
        user = self.users.get(identifier.address)
        if user is not None:
            return user
        # 3. get from delegate
        if self.delegate is not None:
            account = self.delegate.account(identifier=identifier)
        if account is None:
            # 4. create directory
            account = Account(identifier=identifier)
        # 5. cache
        self.cache_account(account=account)
        return account

    def user(self, identifier: ID) -> User:
        # 1. get from user cache
        user = self.users.get(identifier.address)
        if user is not None:
            return user
        # 2. get from delegate
        if self.delegate is not None:
            user = self.delegate.user(identifier=identifier)
        if user is None:
            # 3. create directory
            user = User(identifier=identifier)
        # 4. cache
        self.cache_user(user=user)
        return user

    def group(self, identifier: ID) -> Group:
        # 1. get from group cache
        group = self.groups.get(identifier.address)
        if group is not None:
            return group
        # 2. get from delegate
        if self.delegate is not None:
            group = self.delegate.group(identifier=identifier)
        if group is None:
            # 3. create directory
            group = Group(identifier=identifier)
        # 4. cache
        self.cache_group(group=group)
        return group

    #
    #   IEntityDataSource
    #
    def meta(self, identifier: ID) -> Meta:
        # 1. get from meta cache
        meta = self.metas.get(identifier.address)
        if meta is not None:
            return meta
        # 2. get from entity data source
        meta = self.entityDataSource.meta(identifier=identifier)
        if meta is not None and meta.match_identifier(identifier):
            self.metas[identifier.address] = meta
            return meta

    def profile(self, identifier: ID) -> Profile:
        # NOTICE: do not cache profile here
        return self.entityDataSource.profile(identifier=identifier)

    #
    #   IUserDataSource
    #
    def private_key_for_signature(self, identifier: ID) -> PrivateKey:
        # TODO: signature key will never change, cache it
        return self.userDataSource.private_key_for_signature(identifier=identifier)

    def private_keys_for_decryption(self, identifier: ID) -> list:
        # NOTICE: decryption key can be change, do not cache it here
        return self.userDataSource.private_keys_for_decryption(identifier=identifier)

    def contacts(self, identifier: ID) -> list:
        # NOTICE: do not cache contacts here
        return self.userDataSource.contacts(identifier=identifier)

    #
    #   IGroupDataSource
    #
    def founder(self, identifier: ID) -> ID:
        # TODO: group founder will never change, cache it
        return self.groupDataSource.founder(identifier=identifier)

    def owner(self, identifier: ID) -> ID:
        # NOTICE: do not cache group owner here
        return self.groupDataSource.owner(identifier=identifier)

    def members(self, identifier: ID) -> list:
        # NOTICE: do not cache group members here
        return self.groupDataSource.members(identifier=identifier)


#
#  Delegate
#

class IBarrackDelegate(metaclass=ABCMeta):

    def account(self, identifier: ID) -> Account:
        """ Account factory """
        pass

    def user(self, identifier: ID) -> User:
        """ User factory """
        pass

    def group(self, identifier: ID) -> Group:
        """ Group factory """
        pass


#
#  singleton
#
barrack = Barrack()
