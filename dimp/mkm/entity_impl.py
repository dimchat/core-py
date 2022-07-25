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

import weakref
from typing import Optional

from mkm import ID, Meta, Document

from .entity import Entity, EntityDataSource


class BaseEntity(Entity):

    def __init__(self, identifier: ID):
        """
        Create Entity with ID

        :param identifier: User/Group ID
        """
        super().__init__()
        self.__identifier = identifier
        self.__data_source = None

    def __str__(self):
        clazz = self.__class__.__name__
        return '<%s|%s %s/>' % (clazz, self.type, self.identifier)

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if isinstance(other, Entity):
            other = other.identifier
        return self.__identifier == other

    @property  # Override
    def data_source(self) -> Optional[EntityDataSource]:
        if self.__data_source is not None:
            return self.__data_source()

    @data_source.setter  # Override
    def data_source(self, delegate: EntityDataSource):
        self.__data_source = weakref.ref(delegate)

    @property  # Override
    def identifier(self) -> ID:
        return self.__identifier

    @property  # Override
    def type(self) -> int:
        """ Entity type """
        return self.__identifier.type

    @property  # Override
    def meta(self) -> Meta:
        delegate = self.data_source
        # assert delegate is not None, 'entity delegate not set yet'
        return delegate.meta(identifier=self.identifier)

    # Override
    def document(self, doc_type: Optional[str] = '*') -> Optional[Document]:
        delegate = self.data_source
        # assert delegate is not None, 'entity delegate not set yet'
        return delegate.document(identifier=self.identifier, doc_type=doc_type)
