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
        self.__id = identifier
        self.__barrack = None

    # Override
    def __str__(self):
        """ Return str(self). """
        clazz = self.__class__.__name__
        identifier = self.identifier
        network = identifier.address.type
        return '<%s id="%s" network=%d />' % (clazz, identifier, network)

    # Override
    def __eq__(self, other) -> bool:
        """ Return self==value. """
        if isinstance(other, Entity):
            if self is other:
                # same object
                return True
            other = other.identifier
        # check with ID
        return self.__id.__eq__(other)

    # Override
    def __ne__(self, other) -> bool:
        """ Return self!=value. """
        if isinstance(other, Entity):
            if self is other:
                # same object
                return False
            other = other.identifier
        # check with ID
        return self.__id.__ne__(other)

    @property  # Override
    def data_source(self) -> Optional[EntityDataSource]:
        if self.__barrack is not None:
            return self.__barrack()

    @data_source.setter  # Override
    def data_source(self, barrack: EntityDataSource):
        self.__barrack = weakref.ref(barrack)

    @property  # Override
    def identifier(self) -> ID:
        return self.__id

    @property  # Override
    def type(self) -> int:
        """ Entity type """
        return self.__id.type

    @property  # Override
    def meta(self) -> Meta:
        delegate = self.data_source
        # assert delegate is not None, 'entity delegate not set yet'
        return delegate.meta(identifier=self.__id)

    # Override
    def document(self, doc_type: str = '*') -> Optional[Document]:
        delegate = self.data_source
        # assert delegate is not None, 'entity delegate not set yet'
        return delegate.document(identifier=self.__id, doc_type=doc_type)
