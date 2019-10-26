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

from mkm import ID, Meta, Profile, PrivateKey, NetworkID, is_broadcast
from mkm import User, Group
from mkm import IUserDataSource, IGroupDataSource

from .delegate import ISocialNetworkDataSource


def thanos(planet: dict, finger: int) -> int:
    """ Thanos can kill half lives of a world with a snap of the finger """
    keys = planet.keys()
    for key in keys:
        if (++finger & 1) == 1:
            # kill it
            planet.pop(key)
    return finger


class Barrack(ISocialNetworkDataSource, IUserDataSource, IGroupDataSource):

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
        assert identifier.valid, 'failed to cache ID: %s' % identifier
        self.__ids[identifier] = identifier
        return True

    def cache_meta(self, meta: Meta, identifier: ID) -> bool:
        assert meta is not None and identifier.valid, 'failed to cache meta: %s, %s' % (identifier, meta)
        if meta.match_identifier(identifier):
            self.__metas[identifier] = meta
            return True

    def cache_user(self, user: User) -> bool:
        assert user is not None and user.identifier.valid, 'failed to cache user: %s' % user
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
    #   ISocialNetworkDataSource
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
            try:
                identifier = ID(string)
            except AttributeError:
                # ID string not valid
                pass
            except ValueError:
                # search number(check code) not valid
                pass
            if identifier is not None:
                self.cache_id(identifier=identifier)
                return identifier

    def user(self, identifier: ID) -> User:
        if identifier is not None:
            assert identifier.valid, 'failed to get user with invalid ID: %s' % identifier
            # 1. get from user cache
            usr = self.__users.get(identifier)
            if usr is None and is_broadcast(identifier=identifier):
                # 2. create user 'anyone@anywhere'
                usr = User(identifier=identifier)
                self.cache_user(user=usr)
            return usr

    def group(self, identifier: ID) -> Group:
        if identifier is not None:
            assert identifier.valid, 'failed to get group with invalid ID: %s' % identifier
            # 1. get from group cache
            grp = self.__groups.get(identifier)
            if grp is None and is_broadcast(identifier=identifier):
                # 2. create group 'everyone@everywhere'
                grp = Group(identifier=identifier)
                self.cache_group(group=grp)
            return grp

    #
    #   IEntityDataSource
    #
    def meta(self, identifier: ID) -> Meta:
        if identifier is not None:
            assert identifier.valid, 'failed to get meta with invalid ID: %s' % identifier
            return self.__metas.get(identifier)

    @abstractmethod
    def profile(self, identifier: ID) -> Profile:
        pass

    #
    #   IUserDataSource
    #
    @abstractmethod
    def private_key_for_signature(self, identifier: ID) -> PrivateKey:
        pass

    @abstractmethod
    def private_keys_for_decryption(self, identifier: ID) -> list:
        pass

    @abstractmethod
    def contacts(self, identifier: ID) -> list:
        pass

    #
    #   IGroupDataSource
    #
    @abstractmethod
    def founder(self, identifier: ID) -> ID:
        assert identifier.type.is_group(), 'group ID error: %s' % identifier
        # check for broadcast
        if is_broadcast(identifier=identifier):
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

    @abstractmethod
    def owner(self, identifier: ID) -> ID:
        # check for broadcast
        if is_broadcast(identifier=identifier):
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
        # check group type
        if identifier.type.value == NetworkID.Polylogue:
            # Polylogue's owner is the founder
            return self.founder(identifier=identifier)

    @abstractmethod
    def members(self, identifier: ID) -> list:
        # check for broadcast
        if is_broadcast(identifier=identifier):
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
