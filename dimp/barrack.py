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
from mkm import EntityType, ID

from .protocol import Visa, Bulletin

from .mkm.helper import thanos
from .mkm.helper import DocumentHelper, BroadcastHelper

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
    async def create_user(self, identifier: ID) -> Optional[User]:
        """
        Create user when visa.key exists

        :param identifier: user ID
        :return: user, None on not ready
        """
        raise NotImplemented

    @abstractmethod  # protected
    async def create_group(self, identifier: ID) -> Optional[Group]:
        """
        Create group when members exist

        :param identifier: group ID
        :return: group, None on not ready
        """
        raise NotImplemented

    # protected
    async def get_visa_key(self, identifier: ID) -> Optional[EncryptKey]:
        visa = await self.get_visa(identifier=identifier)
        if visa is not None:  # and visa.valid:
            return visa.public_key

    # protected
    async def get_meta_key(self, identifier: ID) -> Optional[VerifyKey]:
        meta = await self.get_meta(identifier=identifier)
        if meta is not None:  # and meta.valid:
            return meta.public_key

    async def get_visa(self, identifier: ID) -> Optional[Visa]:
        """ Get last visa document """
        documents = await self.get_documents(identifier=identifier)
        return DocumentHelper.last_visa(documents=documents)

    async def get_bulletin(self, identifier: ID) -> Optional[Bulletin]:
        """ get last bulletin document """
        documents = await self.get_documents(identifier=identifier)
        return DocumentHelper.last_bulletin(documents=documents)

    #
    #   Entity Delegate
    #

    # Override
    async def get_user(self, identifier: ID) -> Optional[User]:
        # 1. get from user cache
        usr = self.__users.get(identifier)
        if usr is None:
            # 2. create and cache it
            usr = await self.create_user(identifier=identifier)
            if usr is not None:
                self.cache_user(user=usr)
        return usr

    # Override
    async def get_group(self, identifier: ID) -> Optional[Group]:
        # 1. get from group cache
        grp = self.__groups.get(identifier)
        if grp is None:
            # 2. create and cache it
            grp = await self.create_group(identifier=identifier)
            if grp is not None:
                self.cache_group(group=grp)
        return grp

    #
    #   UserDataSource
    #

    # Override
    async def public_key_for_encryption(self, identifier: ID) -> Optional[EncryptKey]:
        # 1. get key from visa
        key = await self.get_visa_key(identifier=identifier)
        if key is not None:
            # if visa.key exists, use it for encryption
            return key
        # 2. get key from meta
        key = await self.get_meta_key(identifier=identifier)
        if isinstance(key, EncryptKey):
            # if visa.key not exists and meta.key is encrypt key,
            # use it for encryption
            return key

    # Override
    async def public_keys_for_verification(self, identifier: ID) -> List[VerifyKey]:
        keys = []
        # 1. get key from meta
        key = await self.get_meta_key(identifier=identifier)
        if key is not None:
            # the sender may use identity key to sign message.data,
            # try to verify it with meta.key
            keys.append(key)
        # 2. get key from visa
        key = await self.get_visa_key(identifier=identifier)
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
    async def get_founder(self, identifier: ID) -> Optional[ID]:
        # check for broadcast
        if identifier.is_broadcast:
            # founder of broadcast group
            return BroadcastHelper.broadcast_founder(group=identifier)
        # get from document
        doc = await self.get_bulletin(identifier=identifier)
        if doc is not None:  # and doc.valid:
            return doc.founder
        # TODO: load founder from database

    # Override
    async def get_owner(self, identifier: ID) -> Optional[ID]:
        # check for broadcast
        if identifier.is_broadcast:
            # owner of broadcast group
            return BroadcastHelper.broadcast_owner(group=identifier)
        # check group type
        if identifier.type == EntityType.GROUP:
            # Polylogue's owner is its founder
            return await self.get_founder(identifier=identifier)
        # TODO: load owner from database

    # Override
    async def get_members(self, identifier: ID) -> List[ID]:
        # check for broadcast
        if identifier.is_broadcast:
            # members of broadcast group
            return BroadcastHelper.broadcast_members(group=identifier)
        # TODO: load members from database
        return []

    # Override
    async def get_assistants(self, identifier: ID) -> List[ID]:
        doc = await self.get_bulletin(identifier=identifier)
        if doc is not None:  # and doc.valid:
            bots = doc.assistants
            if bots is not None:
                return bots
        # TODO: get group bots from SP configuration
        return []
