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
        key = str(identifier.address)
        return self.metas.get(key)

    def retain_meta(self, meta: Meta, identifier: ID) -> bool:
        if meta.match_identifier(identifier):
            key = str(identifier.address)
            self.metas[key] = meta
            return True
        else:
            return False

    # profile
    def profile(self, identifier: ID) -> dict:
        key = str(identifier.address)
        return self.profiles.get(key)

    def retain_profile(self, profile: dict, identifier: ID) -> bool:
        if profile is not None:
            key = str(identifier.address)
            self.profiles[key] = profile
            return True
        else:
            return False

    # private key
    def private_key(self, identifier: ID) -> PrivateKey:
        key = str(identifier.address)
        return self.private_keys.get(key)

    def retain_private_key(self, private_key: PrivateKey, identifier: ID):
        key = str(identifier.address)
        self.private_keys[key] = private_key

    # account
    def account(self, identifier: ID) -> Account:
        key = str(identifier)
        return self.accounts.get(key)

    def retain_account(self, account: Account):
        key = str(account.identifier)
        self.accounts[key] = account
        # delegate
        if account.delegate is None:
            account.delegate = self

    # group
    def group(self, identifier: ID) -> Group:
        key = str(identifier)
        return self.groups.get(key)

    def retain_group(self, group: Group):
        key = str(group.identifier)
        self.groups[key] = group
        # delegate
        if group.delegate is None:
            group.delegate = self

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
            if len(names) > 0:
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
        self.retain_account(entity)
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
        self.retain_group(entity)
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
