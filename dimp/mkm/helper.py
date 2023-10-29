# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2023 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2023 Albert Moky
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

from abc import ABC
from typing import Optional, List

from mkm.types import DateTime
from mkm import ID, ANYONE, FOUNDER
from mkm import Document

from ..protocol import Visa, Bulletin


def thanos(planet: dict, finger: int) -> int:
    """ Thanos can kill half lives of a world with a snap of the finger """
    people = planet.keys()
    for anybody in people:
        if (++finger & 1) == 1:
            # kill it
            planet.pop(anybody)
    return finger


class BroadcastHelper(ABC):

    @classmethod  # private
    def group_seed(cls, group: ID) -> Optional[str]:
        name = group.name
        if name is not None:
            length = len(name)
            if length > 0 and (length != 8 or name.lower() != 'everyone'):
                return name

    @classmethod  # protected
    def broadcast_founder(cls, group: ID) -> Optional[ID]:
        name = cls.group_seed(group=group)
        if name is None:
            # Consensus: the founder of group 'everyone@everywhere'
            #            'Albert Moky'
            return FOUNDER
        else:
            # DISCUSS: who should be the founder of group 'xxx@everywhere'?
            #          'anyone@anywhere', or 'xxx.founder@anywhere'
            return ID.parse(identifier=name + '.founder@anywhere')

    @classmethod  # protected
    def broadcast_owner(cls, group: ID) -> Optional[ID]:
        name = cls.group_seed(group=group)
        if name is None:
            # Consensus: the owner of group 'everyone@everywhere'
            #            'anyone@anywhere'
            return ANYONE
        else:
            # DISCUSS: who should be the owner of group 'xxx@everywhere'?
            #          'anyone@anywhere', or 'xxx.owner@anywhere'
            return ID.parse(identifier=name + '.owner@anywhere')

    @classmethod  # protected
    def broadcast_members(cls, group: ID) -> List[ID]:
        name = cls.group_seed(group=group)
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


class DocumentHelper(ABC):

    @classmethod
    def is_before(cls, old_time: Optional[DateTime], this_time: Optional[DateTime]) -> bool:
        """ Check whether this time is before old time """
        if old_time is not None and this_time is not None:
            return this_time.before(old_time)

    @classmethod
    def is_expired(cls, this_doc: Document, old_doc: Document) -> bool:
        """ Check whether this document's time is before old document's time """
        return cls.is_before(old_time=old_doc.time, this_time=this_doc.time)

    @classmethod
    def last_document(cls, documents: List[Document], doc_type: str = None) -> Optional[Document]:
        """ Select last document matched the type """
        if doc_type is None or doc_type == '*':
            doc_type = ''
        check_type = len(doc_type) > 0
        last: Optional[Document] = None
        for item in documents:
            # 1. check type
            if check_type:
                item_type = item.type
                if item_type is not None and len(item_type) > 0 and item_type != doc_type:
                    # type not matched, skip it
                    continue
            # 2. check time
            if last is not None:
                if cls.is_expired(this_doc=item, old_doc=last):
                    # skip expired document
                    continue
            # got it
            last = item
        return last

    @classmethod
    def last_visa(cls, documents: List[Document]) -> Optional[Visa]:
        """ Select last visa document """
        last: Optional[Visa] = None
        for item in documents:
            # 1. check type
            if not isinstance(item, Visa):
                # type not matched, skip it
                continue
            # 2. check time
            if last is not None and cls.is_expired(this_doc=item, old_doc=last):
                # skip expired document
                continue
            # got it
            last = item
        return last

    @classmethod
    def last_bulletin(cls, documents: List[Document]) -> Optional[Bulletin]:
        """ Select last bulletin document """
        last: Optional[Bulletin] = None
        for item in documents:
            # 1. check type
            if not isinstance(item, Bulletin):
                # type not matched, skip it
                continue
            # 2. check time
            if last is not None and cls.is_expired(this_doc=item, old_doc=last):
                # skip expired document
                continue
            # got it
            last = item
        return last
