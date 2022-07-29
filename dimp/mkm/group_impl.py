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

from typing import Optional, List

from mkm import ID, Document, Bulletin

from .group import Group, GroupDataSource
from .entity_impl import BaseEntity


class BaseGroup(BaseEntity, Group):

    def __init__(self, identifier: ID):
        super().__init__(identifier=identifier)
        # once the group founder is set, it will never change
        self.__founder = None

    @BaseEntity.data_source.getter  # Override
    def data_source(self) -> Optional[GroupDataSource]:
        return super().data_source

    # @data_source.setter  # Override
    # def data_source(self, delegate: GroupDataSource):
    #     super(BaseGroup, BaseGroup).data_source.__set__(self, delegate)

    @property  # Override
    def bulletin(self) -> Optional[Bulletin]:
        doc = self.document(doc_type=Document.BULLETIN)
        if isinstance(doc, Bulletin):
            return doc

    @property  # Override
    def founder(self) -> ID:
        if self.__founder is None:
            delegate = self.data_source
            # assert delegate is not None, 'group delegate not set yet'
            self.__founder = delegate.founder(identifier=self.identifier)
        return self.__founder

    @property  # Override
    def owner(self) -> ID:
        delegate = self.data_source
        # assert delegate is not None, 'group delegate not set yet'
        return delegate.owner(identifier=self.identifier)

    @property  # Override
    def members(self) -> List[ID]:
        delegate = self.data_source
        # assert delegate is not None, 'group delegate not set yet'
        return delegate.members(identifier=self.identifier)

    @property  # Override
    def assistants(self) -> List[ID]:
        delegate = self.data_source
        # assert delegate is not None, 'group delegate not set yet'
        return delegate.assistants(identifier=self.identifier)
