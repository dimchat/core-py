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

from abc import ABC
from typing import Optional, List

from mkm import ID

from .history import HistoryCommand


class GroupCommand(HistoryCommand, ABC):
    """
        Group Command
        ~~~~~~~~~~~~~

        data format: {
            type : 0x89,
            sn   : 123,

            cmd     : "invite",         // "expel", "quit"
            time    : 0,                // timestamp
            group   : "{GROUP_ID}",     // group ID
            member  : "{MEMBER_ID}",    // member ID
            members : ["{MEMBER_ID}",], // member ID list
        }
    """

    # -------- command names begin --------
    # founder/owner
    FOUND = "found"
    ABDICATE = "abdicate"
    # member
    INVITE = "invite"
    EXPEL = "expel"
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
    def member(self) -> Optional[ID]:
        raise NotImplemented

    @member.setter
    def member(self, value: ID):
        raise NotImplemented

    @property
    def members(self) -> Optional[List[ID]]:
        raise NotImplemented

    @members.setter
    def members(self, value: List[ID]):
        raise NotImplemented

    #
    #   Factory methods
    #

    @classmethod
    def invite(cls, group: ID, member: Optional[ID] = None, members: Optional[List[ID]] = None):
        from ..dkd import InviteGroupCommand
        return InviteGroupCommand(group=group, member=member, members=members)

    @classmethod
    def expel(cls, group: ID, member: Optional[ID] = None, members: Optional[List[ID]] = None):
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
    def query(cls, group: ID):
        from ..dkd import QueryGroupCommand
        return QueryGroupCommand(group=group)

    @classmethod
    def reset(cls, group: ID, members: Optional[List[ID]] = None):
        from ..dkd import ResetGroupCommand
        return ResetGroupCommand(group=group, members=members)


class InviteCommand(GroupCommand, ABC):
    pass


class ExpelCommand(GroupCommand, ABC):
    pass


class JoinCommand(GroupCommand, ABC):
    pass


class QuitCommand(GroupCommand, ABC):
    pass


class QueryCommand(GroupCommand, ABC):
    pass


class ResetCommand(GroupCommand, ABC):
    pass
