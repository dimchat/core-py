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

from typing import Optional, Any, Dict, List

from mkm import ID

from ..protocol import GroupCommand
from ..protocol import InviteCommand, ExpelCommand, JoinCommand, QuitCommand, QueryCommand, ResetCommand

from .history import BaseHistoryCommand


class BaseGroupCommand(BaseHistoryCommand, GroupCommand):
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

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 cmd: Optional[str] = None, group: Optional[ID] = None,
                 member: Optional[ID] = None, members: Optional[List[ID]] = None):
        super().__init__(content=content, cmd=cmd)
        if group is not None:
            self.group = group
        if member is not None:
            self.member = member
        elif members is not None:
            self.members = members

    #
    #   group (group ID already fetched in Content)
    #

    #
    #   member/members
    #
    @property  # Override
    def member(self) -> Optional[ID]:
        return ID.parse(identifier=self.get('member'))

    @member.setter  # Override
    def member(self, value: ID):
        if value is None:
            self.pop('member', None)
        else:
            self['member'] = str(value)

    @property  # Override
    def members(self) -> Optional[List[ID]]:
        array = self.get('members')
        if array is not None:
            # convert all items to ID objects
            return ID.convert(members=array)

    @members.setter  # Override
    def members(self, value: List[ID]):
        if value is None:
            self.pop('members', None)
        else:
            self['members'] = ID.revert(members=value)


class InviteGroupCommand(BaseGroupCommand, InviteCommand):

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 group: Optional[ID] = None,
                 member: Optional[ID] = None, members: Optional[List[ID]] = None):
        """
        Create invite group member command

        :param content: command content
        :param group:   group ID
        :param member:  member ID
        :param members: member list
        :return: InviteCommand object
        """
        super().__init__(content=content, cmd=GroupCommand.INVITE,
                         group=group, member=member, members=members)


class ExpelGroupCommand(BaseGroupCommand, ExpelCommand):

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 group: Optional[ID] = None,
                 member: Optional[ID] = None, members: Optional[List[ID]] = None):
        """
        Create expel group member command

        :param content: command content
        :param group:   group ID
        :param member:  member ID
        :param members: member list
        :return: ExpelCommand object
        """
        super().__init__(content=content, cmd=GroupCommand.EXPEL,
                         group=group, member=member, members=members)


class JoinGroupCommand(BaseGroupCommand, JoinCommand):

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 group: Optional[ID] = None):
        """
        Create join group command

        :param content: command content
        :param group:   group ID
        :return: JoinCommand object
        """
        super().__init__(content=content, cmd=GroupCommand.JOIN,
                         group=group)


class QuitGroupCommand(BaseGroupCommand, QuitCommand):

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 group: Optional[ID] = None):
        """
        Create member quit command

        :param content: command content
        :param group:   group ID
        :return: QuitCommand object
        """
        super().__init__(content=content, cmd=GroupCommand.QUIT,
                         group=group)


class QueryGroupCommand(BaseGroupCommand, QueryCommand):

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 group: Optional[ID] = None):
        """
        Create query group members command (not history command)

        :param content: command content
        :param group:   group ID
        :return: QueryCommand object
        """
        super().__init__(content=content, cmd=GroupCommand.QUERY,
                         group=group)


class ResetGroupCommand(BaseGroupCommand, ResetCommand):

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 group: Optional[ID] = None,
                 members: Optional[List[ID]] = None):
        """
        Create reset group members command

        :param content: command content
        :param group:   group ID
        :param members: member list
        :return: ResetCommand object
        """
        super().__init__(content=content, cmd=GroupCommand.RESET,
                         group=group, members=members)
