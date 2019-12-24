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

from abc import abstractmethod
from typing import Optional

from mkm import EncryptKey, SignKey
from mkm import ID, Meta
from mkm import User, Group
from mkm import UserDataSource, GroupDataSource

from .delegate import EntityDelegate


def thanos(planet: dict, finger: int) -> int:
    """ Thanos can kill half lives of a world with a snap of the finger """
    keys = planet.keys()
    for key in keys:
        if (++finger & 1) == 1:
            # kill it
            planet.pop(key)
    return finger


class Barrack(EntityDelegate, UserDataSource, GroupDataSource):

    def __init__(self):
        super().__init__()
        # memory caches
        self.__ids = {}
        self.__metas = {}
        self.__users = {}
        self.__groups = {}

    def reduce_memory(self) -> int:
        """
        Call it when received 'UIApplicationDidReceiveMemoryWarningNotification',
        this will remove 50% of cached objects

        :return: number of survivors
        """
        finger = 0
        finger = thanos(self.__ids, finger)
        finger = thanos(self.__metas, finger)
        finger = thanos(self.__users, finger)
        finger = thanos(self.__groups, finger)
        return finger >> 1

    def cache_id(self, identifier: ID) -> bool:
        assert identifier.valid, 'ID not valid: %s' % identifier
        self.__ids[identifier] = identifier
        return True

    def cache_meta(self, meta: Meta, identifier: ID) -> bool:
        assert meta.match_identifier(identifier), 'meta not match ID: %s, %s' % (identifier, meta)
        self.__metas[identifier] = meta
        return True

    def cache_user(self, user: User) -> bool:
        if user.delegate is None:
            user.delegate = self
        self.__users[user.identifier] = user
        return True

    def cache_group(self, group: Group) -> bool:
        if group.delegate is None:
            group.delegate = self
        self.__groups[group.identifier] = group
        return True

    def create_identifier(self, string: str) -> ID:
        assert isinstance(string, str), 'ID error: %s' % string
        return ID(string)

    def create_user(self, identifier: ID) -> User:
        assert identifier.type.is_user(), 'user ID error: %s' % identifier
        if identifier.is_broadcast:
            # create user 'anyone@anywhere'
            return User(identifier=identifier)
        # make sure meta exists
        assert self.meta(identifier) is not None, 'failed to get meta for user: %s' % identifier
        # TODO: check user type
        return User(identifier=identifier)

    def create_group(self, identifier: ID) -> Group:
        assert identifier.type.is_group(), 'group ID error: %s' % identifier
        if identifier.is_broadcast:
            # create group 'everyone@everywhere'
            return Group(identifier=identifier)
        # make sure meta exists
        assert self.meta(identifier) is not None, 'failed to get meta for group: %s' % identifier
        # TODO: check group type
        return Group(identifier=identifier)

    #
    #   EntityDelegate
    #
    def identifier(self, string: str) -> Optional[ID]:
        if string is None:
            return None
        elif isinstance(string, ID):
            return string
        assert isinstance(string, str), 'ID string error: %s' % string
        # 1. get from ID cache
        identifier = self.__ids.get(string)
        if identifier is not None:
            return identifier
        # 2. create and cache it
        identifier = self.create_identifier(string=string)
        if identifier is not None and self.cache_id(identifier=identifier):
            return identifier

    def user(self, identifier: ID) -> Optional[User]:
        # 1. get from user cache
        usr = self.__users.get(identifier)
        if usr is not None:
            return usr
        # 2. create and cache it
        usr = self.create_user(identifier=identifier)
        if usr is not None and self.cache_user(user=usr):
            return usr

    def group(self, identifier: ID) -> Optional[Group]:
        # 1. get from group cache
        grp = self.__groups.get(identifier)
        if grp is not None:
            return grp
        # 2. create and cache it
        grp = self.create_group(identifier=identifier)
        if grp is not None and self.cache_group(group=grp):
            return grp

    #
    #   EntityDataSource
    #
    def meta(self, identifier: ID) -> Optional[Meta]:
        assert identifier.valid, 'entity ID error: %s' % identifier
        return self.__metas.get(identifier)

    #
    #   UserDataSource
    #
    def public_key_for_encryption(self, identifier: ID) -> EncryptKey:
        # NOTICE: return nothing to use profile.key or meta.key
        pass

    @abstractmethod
    def private_keys_for_decryption(self, identifier: ID) -> Optional[list]:
        raise NotImplemented

    @abstractmethod
    def private_key_for_signature(self, identifier: ID) -> Optional[SignKey]:
        raise NotImplemented

    def public_keys_for_verification(self, identifier: ID) -> list:
        # NOTICE: return nothing to use meta.key
        pass

    #
    #   GroupDataSource
    #
    def founder(self, identifier: ID) -> Optional[ID]:
        assert identifier.type.is_group(), 'group ID error: %s' % identifier
        # check for broadcast
        if identifier.is_broadcast:
            name = identifier.name
            if name is None:
                length = 0
            else:
                length = len(name)
            if length == 0 or (length == 8 and name == 'everyone'):
                # Consensus: the founder of group 'everyone@everywhere'
                #            'Albert Moky'
                founder = 'moky@anywhere'
            else:
                # DISCUSS: who should be the founder of group 'xxx@everywhere'?
                #          'anyone@anywhere', or 'xxx.founder@anywhere'
                founder = name + '.founder@anywhere'
            return self.identifier(string=founder)

    def owner(self, identifier: ID) -> Optional[ID]:
        assert identifier.type.is_group(), 'group ID error: %s' % identifier
        # check for broadcast
        if identifier.is_broadcast:
            name = identifier.name
            if name is None:
                length = 0
            else:
                length = len(name)
            if length == 0 or (length == 8 and name == 'everyone'):
                # Consensus: the owner of group 'everyone@everywhere'
                #            'anyone@anywhere'
                owner = 'anyone@anywhere'
            else:
                # DISCUSS: who should be the owner of group 'xxx@everywhere'?
                #          'anyone@anywhere', or 'xxx.owner@anywhere'
                owner = name + '.owner@anywhere'
            return self.identifier(string=owner)

    def members(self, identifier: ID) -> Optional[list]:
        assert identifier.type.is_group(), 'group ID error: %s' % identifier
        # check for broadcast
        if identifier.is_broadcast:
            name = identifier.name
            if name is None:
                length = 0
            else:
                length = len(name)
            if length == 0 or (length == 8 and name == 'everyone'):
                # Consensus: the member of group 'everyone@everywhere'
                #            'anyone@anywhere'
                member = 'anyone@anywhere'
            else:
                # DISCUSS: who should be the member of group 'xxx@everywhere'?
                #          'anyone@anywhere', or 'xxx.member@anywhere'
                member = name + '.member@anywhere'
            member = self.identifier(string=member)
            owner = self.owner(identifier=identifier)
            if member == owner:
                return [owner]
            else:
                return [owner, member]
