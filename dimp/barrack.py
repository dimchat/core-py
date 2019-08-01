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
    Entity Database
    ~~~~~~~~~~~~~~~

    Manage meta for all entities
"""

from mkm import PrivateKey
from mkm import ID, Meta, Profile
from mkm import Account, User, Group
from mkm import IEntityDataSource, IUserDataSource, IGroupDataSource

from .delegate import ISocialNetworkDataSource


class Barrack(ISocialNetworkDataSource, IUserDataSource, IGroupDataSource):

    def __init__(self):
        super().__init__()

        # delegates
        self.entityDataSource: IEntityDataSource = None
        self.userDataSource: IUserDataSource = None
        self.groupDataSource: IGroupDataSource = None

        # memory caches
        self.__ids = {}
        self.__metas = {}
        self.__accounts = {}
        self.__users = {}
        self.__groups = {}

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
        assert identifier.valid, 'failed to cache ID: %s' % identifier
        self.__ids[identifier] = identifier
        return True

    def cache_meta(self, meta: Meta, identifier: ID) -> bool:
        assert meta is not None and identifier.valid, 'failed to cache meta: %s, %s' % (identifier, meta)
        if meta.match_identifier(identifier):
            self.__metas[identifier] = meta
            return True

    def cache_account(self, account: Account) -> bool:
        assert account is not None and account.identifier.valid, 'failed to cache account: %s' % account
        if isinstance(account, User):
            return self.cache_user(user=account)
        if account.delegate is None:
            account.delegate = self
        self.__accounts[account.identifier] = account
        return True

    def cache_user(self, user: User) -> bool:
        assert user is not None and user.identifier.valid, 'failed to cache user: %s' % user
        self.__accounts.pop(user.identifier, None)
        if user.delegate is None:
            user.delegate = self
        self.__users[user.identifier] = user
        return True

    def cache_group(self, group: Group) -> bool:
        assert group is not None and group.identifier.valid, 'failed to cache group: %s' % group
        if group.delegate is None:
            group.delegate = self
        self.__groups[group.identifier] = group
        return True

    #
    #   IBarrackDelegate
    #
    def identifier(self, string: str) -> ID:
        if string is not None:
            if isinstance(string, ID):
                return string
            assert isinstance(string, str), 'ID must be a string: %s' % string
            # 1. get from ID cache
            identifier = self.__ids.get(string)
            if identifier is not None:
                return identifier
            # 2. create and cache it
            identifier = ID(identifier=string)
            if identifier is not None:
                self.cache_id(identifier=identifier)
                return identifier

    def account(self, identifier: ID) -> Account:
        if identifier is not None:
            assert identifier.valid, 'failed to get account with invalid ID: %s' % identifier
            # 1. get from account cache
            account = self.__accounts.get(identifier)
            if account is not None:
                return account
            # 2. get from user cache
            return self.__users.get(identifier)

    def user(self, identifier: ID) -> User:
        if identifier is not None:
            assert identifier.valid, 'failed to get user with invalid ID: %s' % identifier
            # 1. get from user cache
            return self.__users.get(identifier)

    def group(self, identifier: ID) -> Group:
        if identifier is not None:
            assert identifier.valid, 'failed to get group with invalid ID: %s' % identifier
            # 1. get from group cache
            return self.__groups.get(identifier)

    #
    #   IEntityDataSource
    #
    def save_meta(self, meta: Meta, identifier: ID) -> bool:
        # 1. cache it
        if self.cache_meta(meta=meta, identifier=identifier):
            # 2. save by delegate
            return self.entityDataSource.save_meta(meta=meta, identifier=identifier)

    def meta(self, identifier: ID) -> Meta:
        if identifier is not None:
            assert identifier.valid, 'failed to get meta with invalid ID: %s' % identifier
            # 1. get from meta cache
            meta = self.__metas.get(identifier)
            if meta is not None:
                return meta
            # 2. get from entity data source
            if self.entityDataSource is not None:
                meta = self.entityDataSource.meta(identifier=identifier)
                # 3. cache it
                if meta is not None:
                    self.cache_meta(meta=meta, identifier=identifier)
            return meta

    def profile(self, identifier: ID) -> Profile:
        if identifier is not None:
            assert identifier.valid, 'failed to get profile with invalid ID: %s' % identifier
            if self.entityDataSource is not None:
                # NOTICE: do not cache profile here
                return self.entityDataSource.profile(identifier=identifier)

    #
    #   IUserDataSource
    #
    def private_key_for_signature(self, identifier: ID) -> PrivateKey:
        if identifier is not None and self.userDataSource is not None:
            assert identifier.valid, 'failed to get private key with invalid ID: %s' % identifier
            # TODO: signature key will never change, cache it
            return self.userDataSource.private_key_for_signature(identifier=identifier)

    def private_keys_for_decryption(self, identifier: ID) -> list:
        if identifier is not None and self.userDataSource is not None:
            assert identifier.valid, 'failed to get private keys with invalid ID: %s' % identifier
            # NOTICE: decryption key can be change, do not cache it here
            return self.userDataSource.private_keys_for_decryption(identifier=identifier)

    def contacts(self, identifier: ID) -> list:
        if identifier is not None and self.userDataSource is not None:
            assert identifier.valid, 'failed to get contacts with invalid user ID: %s' % identifier
            # NOTICE: do not cache contacts here
            return self.userDataSource.contacts(identifier=identifier)

    #
    #   IGroupDataSource
    #
    def founder(self, identifier: ID) -> ID:
        if identifier is not None and self.groupDataSource is not None:
            assert identifier.valid, 'failed to get founder with invalid group ID: %s' % identifier
            assert identifier.type.is_group(), 'ID type is not GROUP'
            # TODO: group founder will never change, cache it
            return self.groupDataSource.founder(identifier=identifier)

    def owner(self, identifier: ID) -> ID:
        if identifier is not None and self.groupDataSource is not None:
            assert identifier.valid, 'failed to get owner with invalid group ID: %s' % identifier
            assert identifier.type.is_group(), 'ID type is not GROUP'
            # NOTICE: do not cache group owner here
            return self.groupDataSource.owner(identifier=identifier)

    def members(self, identifier: ID) -> list:
        if identifier is not None and self.groupDataSource is not None:
            assert identifier.valid, 'failed to get members with invalid group ID: %s' % identifier
            assert identifier.type.is_group(), 'ID type is not GROUP'
            # NOTICE: do not cache group members here
            return self.groupDataSource.members(identifier=identifier)
