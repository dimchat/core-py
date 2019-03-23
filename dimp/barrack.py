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
    User Database
    ~~~~~~~~~~~~~

    Manage meta for all entities
"""

from mkm import PrivateKey

from mkm import Meta, ID
from mkm import Entity, Account, Group
from mkm import IAccountDelegate, IGroupDelegate, IGroupDataSource


class Barrack(IAccountDelegate, IGroupDelegate, IGroupDataSource):

    def __init__(self):
        super().__init__()

        self.metas = {}
        self.profiles = {}
        self.private_keys = {}

        self.accounts = {}
        self.groups = {}

    # meta
    def meta(self, identifier: ID) -> Meta:
        return self.metas.get(identifier.address)

    def cache_meta(self, meta: Meta, identifier: ID) -> bool:
        if meta.match_identifier(identifier):
            self.metas[identifier.address] = meta
            return True
        else:
            return False

    # profile
    def profile(self, identifier: ID) -> dict:
        return self.profiles.get(identifier.address)

    def cache_profile(self, profile: dict, identifier: ID) -> bool:
        if profile is not None:
            self.profiles[identifier.address] = profile
            return True
        else:
            return False

    # private key
    def private_key(self, identifier: ID) -> PrivateKey:
        return self.private_keys.get(identifier.address)

    def cache_private_key(self, private_key: PrivateKey, identifier: ID) -> bool:
        meta = self.meta(identifier=identifier)
        if meta and meta.key.match(private_key=private_key):
            self.private_keys[identifier.address] = private_key
            return True
        else:
            return False

    # account
    def account(self, identifier: ID) -> Account:
        return self.accounts.get(identifier)

    def cache_account(self, account: Account) -> bool:
        self.accounts[account.identifier] = account
        # delegate
        if account.delegate is None:
            account.delegate = self
        return True

    # group
    def group(self, identifier: ID) -> Group:
        return self.groups.get(identifier)

    def cache_group(self, group: Group) -> bool:
        self.groups[group.identifier] = group
        # delegate
        if group.delegate is None:
            group.delegate = self
        return True

    #
    #   IEntityDataSource
    #
    def entity_meta(self, entity: Entity) -> Meta:
        return self.meta(identifier=entity.identifier)

    def entity_name(self, entity: Entity) -> str:
        profile = self.profile(identifier=entity.identifier)
        if profile:
            name = profile.get('name')
            if name is not None:
                return name
            names: list = profile.get('names')
            if names and len(names) > 0:
                return names[0]
        # profile not found
        if entity.identifier.name:
            return entity.identifier.name
        else:
            return entity.identifier.address

    #
    #   IAccountDelegate
    #
    def account_create(self, identifier: ID) -> Account:
        entity = self.account(identifier=identifier)
        if entity:
            return entity
        # create
        entity = Account(identifier=identifier)
        self.cache_account(entity)
        return entity

    #
    #   IGroupDelegate
    #
    def group_create(self, identifier: ID) -> Group:
        entity = self.group(identifier=identifier)
        if entity:
            return entity
        # create
        entity = Group(identifier=identifier)
        self.cache_group(entity)
        return entity

    def group_add_member(self, group: Group, member: ID) -> bool:
        """ Add member to group """
        pass

    def group_remove_member(self, group: Group, member: ID) -> bool:
        """ Remove member from group """
        pass

    #
    #   IGroupDataSource
    #
    def group_founder(self, group: Group) -> ID:
        """ Get founder of the group """
        pass

    def group_owner(self, group: Group) -> ID:
        """ Get current owner of the group """
        pass

    def group_members(self, group: Group) -> list:
        pass
