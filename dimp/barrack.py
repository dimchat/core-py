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

from abc import ABC
from typing import Optional, List

from mkm.crypto import EncryptKey, VerifyKey
from mkm import EntityType, ID, ANYONE, FOUNDER
from mkm import Document, Visa, Bulletin

from .mkm import EntityDelegate, UserDataSource, GroupDataSource


# noinspection PyAbstractClass
class Barrack(EntityDelegate, UserDataSource, GroupDataSource, ABC):

    def __visa_key(self, identifier: ID) -> Optional[EncryptKey]:
        visa = self.document(identifier=identifier, doc_type=Document.VISA)
        if isinstance(visa, Visa):
            if visa.valid:
                return visa.key

    def __meta_key(self, identifier: ID) -> Optional[VerifyKey]:
        meta = self.meta(identifier=identifier)
        if meta is not None:
            return meta.key

    #
    #   UserDataSource
    #

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
    def public_keys_for_verification(self, identifier: ID) -> List[VerifyKey]:
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

    # Override
    def founder(self, identifier: ID) -> Optional[ID]:
        # check for broadcast
        if identifier.is_broadcast:
            # founder of broadcast group
            return broadcast_founder(group=identifier)
        # get from document
        doc = self.document(identifier=identifier, doc_type='*')
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
        doc = self.document(identifier=identifier, doc_type=Document.BULLETIN)
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
        if length > 0 and (length != 8 or name != 'everyone'):
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
