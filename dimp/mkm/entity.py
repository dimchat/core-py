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

from abc import ABC, abstractmethod
from typing import Optional

from mkm import ID, Meta, Document


class EntityDataSource(ABC):
    """ This interface is for getting information for entity(user/group)

        Entity Data Source
        ~~~~~~~~~~~~~~~~~~

        1. meta for user, which is generated by the user's private key
        2. meta for group, which is generated by the founder's private key
        3. meta key, which can verify message sent by this user(or group founder)
        4. visa key, which can encrypt message for the receiver(user)
    """

    @abstractmethod
    def meta(self, identifier: ID) -> Optional[Meta]:
        """
        Get meta for entity ID

        :param identifier: entity ID
        :return:           Meta
        """
        raise NotImplemented

    @abstractmethod
    def document(self, identifier: ID, doc_type: Optional[str] = '*') -> Optional[Document]:
        """
        Get document for entity ID

        :param identifier: entity ID
        :param doc_type:   document type
        :return:           Document
        """
        raise NotImplemented


class Entity(ABC):
    """ Base class of User and Group, ...

        Entity (User/Group)
        ~~~~~~~~~~~~~~~~~~~

            properties:
                identifier - entity ID
                type       - entity type
                meta       - meta for entity ID
                document   - visa for user, or bulletin for group
    """

    @property
    @abstractmethod
    def data_source(self) -> Optional[EntityDataSource]:
        raise NotImplemented

    @data_source.setter
    @abstractmethod
    def data_source(self, delegate: EntityDataSource):
        raise NotImplemented

    @property
    @abstractmethod
    def identifier(self) -> ID:
        raise NotImplemented

    @property
    @abstractmethod
    def type(self) -> int:
        """ Entity type """
        raise NotImplemented

    @property
    @abstractmethod
    def meta(self) -> Meta:
        """ Get meta """
        raise NotImplemented

    @abstractmethod
    def document(self, doc_type: Optional[str] = '*') -> Optional[Document]:
        """ Get document with type """
        raise NotImplemented
