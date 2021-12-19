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

from abc import ABC
from typing import Optional, List

from mkm.crypto import EncryptKey, VerifyKey
from mkm import NetworkType, ID, ANYONE, FOUNDER
from mkm import Meta, Document, Visa, Bulletin

from .user import User, UserDataSource
from .group import GroupDataSource

from .delegate import EntityDelegate


class Barrack(EntityDelegate, UserDataSource, GroupDataSource, ABC):

    @property
    def local_users(self) -> List[User]:
        """
        Get all local users (for decrypting received message)

        :return: users with private key
        """
        raise NotImplemented

    @property
    def current_user(self) -> Optional[User]:
        """ Get current user (for signing and sending message) """
        users = self.local_users
        if users is not None and len(users) > 0:
            return users[0]

    #
    #   EntityDelegate
    #

    # Override
    def select_user(self, receiver: ID) -> Optional[User]:
        users = self.local_users
        assert users is not None and len(users) > 0, 'local users should not be empty'
        if receiver.is_broadcast:
            return users[0]
        if receiver.is_group:
            # group message (recipient not designated)
            members = self.members(identifier=receiver)
            if members is None or len(members) == 0:
                # TODO: group not ready, waiting for group info
                return None
            for item in users:
                assert isinstance(item, User), 'local user error: %s' % item
                if item.identifier in members:
                    # DISCUSS: set this item to be current user?
                    return item
        else:
            # 1. personal message
            # 2. split group message
            for item in users:
                assert isinstance(item, User), 'local user error: %s' % item
                if item.identifier == receiver:
                    # DISCUSS: set this item to be current user?
                    return item

    #
    #   UserDataSource
    #
    def __visa_key(self, identifier: ID) -> Optional[EncryptKey]:
        visa = self.document(identifier=identifier, doc_type=Document.VISA)
        if isinstance(visa, Visa):
            if visa.valid:
                return visa.key

    def __meta_key(self, identifier: ID) -> Optional[VerifyKey]:
        meta = self.meta(identifier=identifier)
        if meta is not None:
            return meta.key

    # Override
    def public_key_for_encryption(self, identifier: ID) -> Optional[EncryptKey]:
        # 1. get key from visa
        key = self.__visa_key(identifier=identifier)
        if key is not None:
            # if visa.key exists, use it for encryption
            return key
        # 2. get key from meta
        key = self.__meta_key(identifier=identifier)
        if isinstance(key, EncryptKey):
            # if visa.key not exists and meta.key is encrypt key,
            # use it for encryption
            return key

    # Override
    def public_keys_for_verification(self, identifier: ID) -> Optional[List[VerifyKey]]:
        keys = []
        # 1. get key from visa
        key = self.__visa_key(identifier=identifier)
        if isinstance(key, VerifyKey):
            # the sender may use communication key to sign message.data,
            # so try to verify it with visa.key here
            keys.append(key)
        # 2. get key from meta
        key = self.__meta_key(identifier=identifier)
        if key is not None:
            # the sender may use identity key to sign message.data,
            # try to verify it with meta.key
            keys.append(key)
        assert len(keys) > 0, 'failed to get verify key for user: %s' % identifier
        return keys

    #
    #   GroupDataSource
    #
    @staticmethod
    def __id_name(identifier) -> Optional[str]:
        name = identifier.name
        if name is not None:
            length = len(name)
            if length > 0 and (length != 8 or name != 'everyone'):
                return name

    def _broadcast_founder(self, identifier: ID) -> Optional[ID]:
        name = self.__id_name(identifier=identifier)
        if name is None:
            # Consensus: the founder of group 'everyone@everywhere'
            #            'Albert Moky'
            return FOUNDER
        else:
            # DISCUSS: who should be the founder of group 'xxx@everywhere'?
            #          'anyone@anywhere', or 'xxx.founder@anywhere'
            return ID.parse(identifier=name + '.founder@anywhere')

    def _broadcast_owner(self, identifier: ID) -> Optional[ID]:
        name = self.__id_name(identifier=identifier)
        if name is None:
            # Consensus: the owner of group 'everyone@everywhere'
            #            'anyone@anywhere'
            return ANYONE
        else:
            # DISCUSS: who should be the owner of group 'xxx@everywhere'?
            #          'anyone@anywhere', or 'xxx.owner@anywhere'
            return ID.parse(identifier=name + '.owner@anywhere')

    def _broadcast_members(self, identifier: ID) -> List[ID]:
        name = self.__id_name(identifier=identifier)
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

    # Override
    def founder(self, identifier: ID) -> Optional[ID]:
        # check for broadcast
        if identifier.is_broadcast:
            # founder of broadcast group
            return self._broadcast_founder(identifier=identifier)
        # check group meta
        g_meta = self.meta(identifier=identifier)
        if g_meta is None:
            # FIXME: when group profile was arrived but the meta still on the way,
            #        here will cause founder not found
            return None
        # check each member's public key with group meta
        members = self.members(identifier=identifier)
        if members is not None:
            for item in members:
                u_meta = self.meta(identifier=item)
                if u_meta is None:
                    # failed to get member's meta
                    continue
                if Meta.matches(meta=g_meta, key=u_meta.key):
                    # if the member's public key matches with the group's meta,
                    # it means this meta was generated by the member's private key
                    return item
        # TODO: load founder from database

    # Override
    def owner(self, identifier: ID) -> Optional[ID]:
        # check for broadcast
        if identifier.is_broadcast:
            # owner of broadcast group
            return self._broadcast_owner(identifier=identifier)
        # check group type
        if identifier.type == NetworkType.POLYLOGUE:
            # Polylogue's owner is its founder
            return self.founder(identifier=identifier)
        # TODO: load owner from database

    # Override
    def members(self, identifier: ID) -> Optional[List[ID]]:
        # check for broadcast
        if identifier.is_broadcast:
            # members of broadcast group
            return self._broadcast_members(identifier=identifier)

    # Override
    def assistants(self, identifier: ID) -> Optional[List[ID]]:
        doc = self.document(identifier=identifier, doc_type=Document.BULLETIN)
        if isinstance(doc, Bulletin):
            if doc.valid:
                return doc.assistants
        # TODO: get group bots from SP configuration
