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
    Group Command Protocol
    ~~~~~~~~~~~~~~~~~~~~~~

    1. invite member
    2. expel member
    3. member quit
"""

from abc import ABC, abstractmethod
from typing import Optional, List

from mkm.types import DateTime
from mkm import ID

from .commands import Command


# noinspection PyAbstractClass
class HistoryCommand(Command, ABC):
    """
        History Command
        ~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x89),
            sn   : 123,

            command : "...", // command name
            time    : 0,     // command timestamp
            extra   : info   // command parameters
        }
    """

    # -------- command names begin --------
    # account
    REGISTER = "register"
    SUICIDE = "suicide"
    # -------- command names end --------


class GroupCommand(HistoryCommand, ABC):
    """
        Group Command
        ~~~~~~~~~~~~~

        data format: {
            type : i2s(0x89),
            sn   : 123,

            command : "reset",   // "invite", "quit", "query", ...
            time    : 0,         // timestamp

            group   : "{GROUP_ID}",
            member  : "{MEMBER_ID}",
            members : ["{MEMBER_ID}",]
        }
    """

    # -------- command names begin --------
    # founder/owner
    FOUND = "found"
    ABDICATE = "abdicate"
    # member
    INVITE = "invite"
    EXPEL = "expel"  # Deprecated (use 'reset' instead)
    JOIN = "join"
    QUIT = "quit"
    RESET = "reset"
    QUERY = "query"  # (not history command)
    # administrator/assistant
    HIRE = "hire"
    FIRE = "fire"
    RESIGN = "resign"
    # -------- command names end --------

    #
    #   group (group ID already fetched in Content)
    #

    #
    #   member/members
    #
    @property
    @abstractmethod
    def member(self) -> Optional[ID]:
        raise NotImplemented

    @member.setter
    @abstractmethod
    def member(self, user: Optional[ID]):
        raise NotImplemented

    @property
    @abstractmethod
    def members(self) -> Optional[List[ID]]:
        raise NotImplemented

    @members.setter
    @abstractmethod
    def members(self, users: Optional[List[ID]]):
        raise NotImplemented

    #
    #   Factory methods
    #

    @classmethod
    def create(cls, cmd: str, group: ID, member: ID = None, members: List[ID] = None):
        from ..dkd import BaseGroupCommand
        return BaseGroupCommand(cmd=cmd, group=group, member=member, members=members)

    @classmethod
    def invite(cls, group: ID, member: ID = None, members: List[ID] = None):
        from ..dkd import InviteGroupCommand
        return InviteGroupCommand(group=group, member=member, members=members)

    @classmethod
    def expel(cls, group: ID, member: ID = None, members: List[ID] = None):
        """ Deprecated (use 'reset' instead) """
        from ..dkd import ExpelGroupCommand
        return ExpelGroupCommand(group=group, member=member, members=members)

    @classmethod
    def join(cls, group: ID):
        from ..dkd import JoinGroupCommand
        return JoinGroupCommand(group=group)

    @classmethod
    def quit(cls, group: ID):
        from ..dkd import QuitGroupCommand
        return QuitGroupCommand(group=group)

    @classmethod
    def query(cls, group: ID, last_time: DateTime = None):
        from ..dkd import QueryGroupCommand
        return QueryGroupCommand(group=group, last_time=last_time)

    @classmethod
    def reset(cls, group: ID, members: List[ID]):
        from ..dkd import ResetGroupCommand
        return ResetGroupCommand(group=group, members=members)

    # Administrators, Assistants

    @classmethod
    def hire(cls, group: ID, administrators: List[ID] = None, assistants: List[ID] = None):
        from ..dkd import HireGroupCommand
        return HireGroupCommand(group=group, administrators=administrators, assistants=assistants)

    @classmethod
    def fire(cls, group: ID, administrators: List[ID] = None, assistants: List[ID] = None):
        from ..dkd import FireGroupCommand
        return FireGroupCommand(group=group, administrators=administrators, assistants=assistants)

    @classmethod
    def resign(cls, group: ID):
        from ..dkd import ResignGroupCommand
        return ResignGroupCommand(group=group)


# noinspection PyAbstractClass
class InviteCommand(GroupCommand, ABC):
    pass


# noinspection PyAbstractClass
class ExpelCommand(GroupCommand, ABC):
    """ Deprecated (use 'reset' instead) """
    pass


# noinspection PyAbstractClass
class JoinCommand(GroupCommand, ABC):
    pass


# noinspection PyAbstractClass
class QuitCommand(GroupCommand, ABC):
    pass


# noinspection PyAbstractClass
class QueryCommand(GroupCommand, ABC):
    """
    NOTICE:
        This command is just for querying group info,
        should not be saved in group history
    """

    @property
    @abstractmethod
    def last_time(self) -> Optional[DateTime]:
        """ Last group history time for querying """
        raise NotImplemented


# noinspection PyAbstractClass
class ResetCommand(GroupCommand, ABC):
    pass


"""
    Administrator
    ~~~~~~~~~~~~~
"""


# noinspection PyAbstractClass
class HireCommand(GroupCommand, ABC):

    @property
    @abstractmethod
    def administrators(self) -> Optional[List[ID]]:
        raise NotImplemented

    @property
    @abstractmethod
    def assistants(self) -> Optional[List[ID]]:
        raise NotImplemented


# noinspection PyAbstractClass
class FireCommand(GroupCommand, ABC):

    @property
    @abstractmethod
    def administrators(self) -> Optional[List[ID]]:
        raise NotImplemented

    @property
    @abstractmethod
    def assistants(self) -> Optional[List[ID]]:
        raise NotImplemented


# noinspection PyAbstractClass
class ResignCommand(GroupCommand, ABC):
    pass
