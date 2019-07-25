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
from typing import Optional

from mkm import PrivateKey
from mkm import ID, Meta, Profile
from mkm import Account, User, Group
from mkm import IEntityDataSource, IUserDataSource, IGroupDataSource

from .delegate import IBarrackDelegate


class Barrack(IBarrackDelegate, IUserDataSource, IGroupDataSource):

    def __init__(self):
        super().__init__()

        # delegates
        self.delegate: IBarrackDelegate = None
        self.entityDataSource: IEntityDataSource = None
        self.userDataSource: IUserDataSource = None
        self.groupDataSource: IGroupDataSource = None

        # memory caches
        self.__ids = {}
        self.__metas = {}
        self.__accounts = {}
        self.__users = {}
        self.__groups = {}

    @property
    def accounts(self) -> dict:
        return self.__accounts

    def reduce_memory(self) -> int:
        """
        Call it when received 'UIApplicationDidReceiveMemoryWarningNotification',
        this will remove 50% of cached objects

        :return: reduced object count
        """
        finger = 0
        finger = self.__thanos(self.__metas, finger)
        finger = self.__thanos(self.__accounts, finger)
        finger = self.__thanos(self.__users, finger)
        finger = self.__thanos(self.__groups, finger)
        return finger >> 1

    @staticmethod
    def __thanos(planet: dict, finger: int) -> int:
        keys = planet.keys()
        for key in keys:
            if (++finger & 1) == 1:
                # kill it
                planet.pop(key)
        return finger

    def cache_id(self, identifier: ID) -> bool:
        assert identifier.valid
        self.__ids[identifier] = identifier
        return True

    def cache_meta(self, meta: Meta, identifier: ID) -> bool:
        if meta.match_identifier(identifier):
            self.__metas[identifier] = meta
            return True

    def cache_account(self, account: Account) -> bool:
        if isinstance(account, User):
            return self.cache_user(user=account)
        if account.delegate is None:
            account.delegate = self
        assert account.identifier.valid
        self.__accounts[account.identifier] = account
        return True

    def cache_user(self, user: User) -> bool:
        self.__accounts.pop(user.identifier, None)
        if user.delegate is None:
            user.delegate = self
        assert user.identifier.valid
        self.__users[user.identifier] = user
        return True

    def cache_group(self, group: Group) -> bool:
        if group.delegate is None:
            group.delegate = self
        assert group.identifier.valid
        self.__groups[group.identifier] = group
        return True

    #
    #   IBarrackDelegate
    #
    def identifier(self, string) -> Optional[ID]:
        if string is None:
            return None
        elif isinstance(string, ID):
            return string
        assert isinstance(string, str)
        # 1. get from ID cache
        value = self.__ids.get(string)
        if value is not None:
            return value
        # 2. get from delegate
        value = self.delegate.identifier(string)
        if value is None:
            # create it directly
            value = ID(identifier=string)
        # 3. cache it
        if value is not None and self.cache_id(identifier=value):
            return value

    def account(self, identifier: ID) -> Optional[Account]:
        if identifier is None:
            return None
        # 1. get from account cache
        account = self.__accounts.get(identifier)
        if account is not None:
            return account
        # 2. get from user cache
        user = self.__users.get(identifier)
        if user is not None:
            return user
        # 3. get from delegate
        account = self.delegate.account(identifier=identifier)
        if account is not None and self.cache_account(account=account):
            return account

    def user(self, identifier: ID) -> Optional[User]:
        if identifier is None:
            return None
        # 1. get from user cache
        user = self.__users.get(identifier)
        if user is not None:
            return user
        # 2. get from delegate
        user = self.delegate.user(identifier=identifier)
        if user is not None and self.cache_user(user=user):
            return user

    def group(self, identifier: ID) -> Optional[Group]:
        if identifier is None:
            return None
        # 1. get from group cache
        group = self.__groups.get(identifier)
        if group is not None:
            return group
        # 2. get from delegate
        group = self.delegate.group(identifier=identifier)
        if group is not None and self.cache_group(group=group):
            return group

    #
    #   IEntityDataSource
    #
    def save_meta(self, meta: Meta, identifier: ID) -> bool:
        # 1. check meta with ID
        if self.cache_meta(meta=meta, identifier=identifier):
            # 2. save by delegate
            return self.entityDataSource.save_meta(meta=meta, identifier=identifier)

    def meta(self, identifier: ID) -> Meta:
        # 1. get from meta cache
        meta = self.__metas.get(identifier)
        if meta is not None:
            return meta
        # 2. get from entity data source
        meta = self.entityDataSource.meta(identifier=identifier)
        if meta is not None and meta.match_identifier(identifier):
            self.__metas[identifier] = meta
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
