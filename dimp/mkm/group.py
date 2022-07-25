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
from typing import Optional, List

from mkm import ID, Bulletin

from .entity import EntityDataSource, Entity


class GroupDataSource(EntityDataSource, ABC):
    """ This interface is for getting information for group

        Group Data Source
        ~~~~~~~~~~~~~~~~~

        1. founder has the same public key with the group's meta.key
        2. owner and members should be set complying with the consensus algorithm
    """

    @abstractmethod
    def founder(self, identifier: ID) -> Optional[ID]:
        """
        Get founder of the group

        :param identifier: group ID
        :return: founder ID
        """
        raise NotImplemented

    @abstractmethod
    def owner(self, identifier: ID) -> Optional[ID]:
        """
        Get current owner of the group

        :param identifier: group ID
        :return: owner ID
        """
        raise NotImplemented

    @abstractmethod
    def members(self, identifier: ID) -> List[ID]:
        """
        Get all members in the group

        :param identifier: group ID
        :return: member ID list
        """
        raise NotImplemented

    @abstractmethod
    def assistants(self, identifier: ID) -> List[ID]:
        """
        Get assistants for this group

        :param identifier: group ID
        :return: robot ID list
        """
        raise NotImplemented


class Group(Entity, ABC):
    """ This class is for creating group

        Group for organizing users
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

            roles:
                founder
                owner
                members
                administrators - Optional
                assistants     - Optional
    """

    @property
    def data_source(self) -> Optional[GroupDataSource]:
        raise NotImplemented

    @data_source.setter
    def data_source(self, delegate: GroupDataSource):
        raise NotImplemented

    @property
    def bulletin(self) -> Optional[Bulletin]:
        raise NotImplemented

    @property
    def founder(self) -> ID:
        raise NotImplemented

    @property
    def owner(self) -> ID:
        raise NotImplemented

    @property
    def members(self) -> List[ID]:
        """ NOTICE: the owner must be a member
            (usually the first one) """
        raise NotImplemented

    @property
    def assistants(self) -> List[ID]:
        raise NotImplemented
