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
    Entity pool to manage User/Contact/Group/Member instances

       1st, get instance here to avoid create same instance,
       2nd, if they were updated, we can refresh them immediately here
"""

from abc import ABC, abstractmethod
from typing import Optional, List

from mkm.crypto import EncryptKey, VerifyKey
from mkm import EntityType, ID, ANYONE, FOUNDER
from mkm import Visa, Bulletin

from .mkm import User, Group
from .mkm import EntityDelegate, UserDataSource, GroupDataSource


class Barrack(EntityDelegate, UserDataSource, GroupDataSource, ABC):

    def __init__(self):
        super().__init__()
        # memory caches
        self.__users = {}   # ID -> User
        self.__groups = {}  # ID -> Group

    # protected
    def cache_user(self, user: User):
        if user.data_source is None:
            user.data_source = self
        self.__users[user.identifier] = user

    # protected
    def cache_group(self, group: Group):
        if group.data_source is None:
            group.data_source = self
        self.__groups[group.identifier] = group

    def reduce_memory(self) -> int:
        """
        Call it when received 'UIApplicationDidReceiveMemoryWarningNotification',
        this will remove 50% of cached objects

        :return: number of survivors
        """
        finger = 0
        finger = thanos(self.__users, finger)
        finger = thanos(self.__groups, finger)
        return finger >> 1

    @abstractmethod  # protected
    def create_user(self, identifier: ID) -> Optional[User]:
        """
        Create user when visa.key exists

        :param identifier: user ID
        :return: user, None on not ready
        """
        raise NotImplemented

    @abstractmethod  # protected
    def create_group(self, identifier: ID) -> Optional[Group]:
        """
        Create group when members exist

        :param identifier: group ID
        :return: group, None on not ready
        """
        raise NotImplemented

    # protected
    def visa_key(self, identifier: ID) -> Optional[EncryptKey]:
        visa = self.document(identifier=identifier)
        if isinstance(visa, Visa):
            if visa.valid:
                return visa.public_key

    # protected
    def meta_key(self, identifier: ID) -> Optional[VerifyKey]:
        meta = self.meta(identifier=identifier)
        if meta is not None:
            return meta.public_key

    #
    #   Entity Delegate
    #

    # Override
    def user(self, identifier: ID) -> Optional[User]:
        # 1. get from user cache
        usr = self.__users.get(identifier)
        if usr is None:
            # 2. create and cache it
            usr = self.create_user(identifier=identifier)
            if usr is not None:
                self.cache_user(user=usr)
        return usr

    # Override
    def group(self, identifier: ID) -> Optional[Group]:
        # 1. get from group cache
        grp = self.__groups.get(identifier)
        if grp is None:
            # 2. create and cache it
            grp = self.create_group(identifier=identifier)
            if grp is not None:
                self.cache_group(group=grp)
        return grp

    #
    #   UserDataSource
    #

    # Override
    def public_key_for_encryption(self, identifier: ID) -> Optional[EncryptKey]:
        # 1. get key from visa
        key = self.visa_key(identifier=identifier)
        if key is not None:
            # if visa.key exists, use it for encryption
            return key
        # 2. get key from meta
        key = self.meta_key(identifier=identifier)
        if isinstance(key, EncryptKey):
            # if visa.key not exists and meta.key is encrypt key,
            # use it for encryption
            return key

    # Override
    def public_keys_for_verification(self, identifier: ID) -> List[VerifyKey]:
        keys = []
        # 1. get key from meta
        key = self.meta_key(identifier=identifier)
        if key is not None:
            # the sender may use identity key to sign message.data,
            # try to verify it with meta.key
            keys.append(key)
        # 2. get key from visa
        key = self.visa_key(identifier=identifier)
        if isinstance(key, VerifyKey):
            # the sender may use communication key to sign message.data,
            # so try to verify it with visa.key here
            keys.append(key)
        assert len(keys) > 0, 'failed to get verify key for user: %s' % identifier
        return keys

    #
    #   GroupDataSource
    #

    # Override
    def founder(self, identifier: ID) -> Optional[ID]:
        # check for broadcast
        if identifier.is_broadcast:
            # founder of broadcast group
            return broadcast_founder(group=identifier)
        # get from document
        doc = self.document(identifier=identifier)
        if isinstance(doc, Bulletin):
            return doc.founder
        # TODO: load founder from database

    # Override
    def owner(self, identifier: ID) -> Optional[ID]:
        # check for broadcast
        if identifier.is_broadcast:
            # owner of broadcast group
            return broadcast_owner(group=identifier)
        # check group type
        if identifier.type == EntityType.GROUP:
            # Polylogue's owner is its founder
            return self.founder(identifier=identifier)
        # TODO: load owner from database

    # Override
    def members(self, identifier: ID) -> List[ID]:
        # check for broadcast
        if identifier.is_broadcast:
            # members of broadcast group
            return broadcast_members(group=identifier)
        # TODO: load members from database
        return []

    # Override
    def assistants(self, identifier: ID) -> List[ID]:
        doc = self.document(identifier=identifier)
        if isinstance(doc, Bulletin) and doc.valid:
            bots = doc.assistants
            if bots is not None:
                return bots
        # TODO: get group bots from SP configuration
        return []


def group_seed(group: ID) -> Optional[str]:
    name = group.name
    if name is not None:
        length = len(name)
        if length > 0 and (length != 8 or name.lower() != 'everyone'):
            return name


def broadcast_founder(group: ID) -> Optional[ID]:
    name = group_seed(group=group)
    if name is None:
        # Consensus: the founder of group 'everyone@everywhere'
        #            'Albert Moky'
        return FOUNDER
    else:
        # DISCUSS: who should be the founder of group 'xxx@everywhere'?
        #          'anyone@anywhere', or 'xxx.founder@anywhere'
        return ID.parse(identifier=name + '.founder@anywhere')


def broadcast_owner(group: ID) -> Optional[ID]:
    name = group_seed(group=group)
    if name is None:
        # Consensus: the owner of group 'everyone@everywhere'
        #            'anyone@anywhere'
        return ANYONE
    else:
        # DISCUSS: who should be the owner of group 'xxx@everywhere'?
        #          'anyone@anywhere', or 'xxx.owner@anywhere'
        return ID.parse(identifier=name + '.owner@anywhere')


def broadcast_members(group: ID) -> List[ID]:
    name = group_seed(group=group)
    if name is None:
        # Consensus: the member of group 'everyone@everywhere'
        #            'anyone@anywhere'
        return [ANYONE]
    else:
        # DISCUSS: who should be the member of group 'xxx@everywhere'?
        #          'anyone@anywhere', or 'xxx.member@anywhere'
        owner = ID.parse(identifier=name + '.owner@anywhere')
        member = ID.parse(identifier=name + '.member@anywhere')
        return [owner, member]


def thanos(planet: dict, finger: int) -> int:
    """ Thanos can kill half lives of a world with a snap of the finger """
    people = planet.keys()
    for anybody in people:
        if (++finger & 1) == 1:
            # kill it
            planet.pop(anybody)
    return finger
