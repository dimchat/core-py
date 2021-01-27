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

from typing import Optional, List

from mkm import ID

from .history import HistoryCommand


class GroupCommand(HistoryCommand):
    """
        Group Command
        ~~~~~~~~~~~~~

        data format: {
            type : 0x89,
            sn   : 123,

            command : "invite",         // "expel", "quit"
            time    : 0,                // timestamp
            group   : "{GROUP_ID}",     // group ID
            member  : "{MEMBER_ID}",    // member ID
            members : ["{MEMBER_ID}",], // member ID list
        }
    """

    def __init__(self, cmd: Optional[dict] = None, command: Optional[str] = None, group: Optional[ID] = None,
                 member: Optional[ID] = None, members: Optional[List[ID]] = None):
        super().__init__(cmd=cmd, command=command)
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
    @property
    def member(self) -> Optional[ID]:
        return ID.parse(identifier=self.get('member'))

    @member.setter
    def member(self, value: ID):
        if value is None:
            self.pop('member', None)
        else:
            self['member'] = str(value)

    @property
    def members(self) -> Optional[List[ID]]:
        array = self.get('members')
        if array is not None:
            # convert all items to ID objects
            return ID.convert(members=array)

    @members.setter
    def members(self, value: List[ID]):
        if value is None:
            self.pop('members', None)
        else:
            self['members'] = ID.revert(members=value)

    @classmethod
    def invite(cls, group: ID, member: Optional[ID] = None, members: Optional[List[ID]] = None):
        return InviteCommand(group=group, member=member, members=members)

    @classmethod
    def expel(cls, group: ID, member: Optional[ID] = None, members: Optional[List[ID]] = None):
        return ExpelCommand(group=group, member=member, members=members)

    @classmethod
    def join(cls, group: ID):
        return JoinCommand(group=group)

    @classmethod
    def quit(cls, group: ID):
        return QuitCommand(group=group)

    @classmethod
    def query(cls, group: ID):
        return QueryCommand(group=group)

    @classmethod
    def reset(cls, group: ID, members: Optional[List[ID]] = None):
        return ResetCommand(group=group, members=members)


class InviteCommand(GroupCommand):

    def __init__(self, cmd: Optional[dict] = None, group: Optional[ID] = None,
                 member: Optional[ID] = None, members: Optional[List[ID]] = None):
        """
        Create invite group member command

        :param cmd:     command info
        :param group:   group ID
        :param member:  member ID
        :param members: member list
        :return: InviteCommand object
        """
        super().__init__(cmd, GroupCommand.INVITE, group=group, member=member, members=members)


class ExpelCommand(GroupCommand):

    def __init__(self, cmd: Optional[dict] = None, group: Optional[ID] = None,
                 member: Optional[ID] = None, members: Optional[List[ID]] = None):
        """
        Create expel group member command

        :param cmd:     command info
        :param group:   group ID
        :param member:  member ID
        :param members: member list
        :return: ExpelCommand object
        """
        super().__init__(cmd, GroupCommand.EXPEL, group=group, member=member, members=members)


class JoinCommand(GroupCommand):

    def __init__(self, cmd: Optional[dict] = None, group: Optional[ID] = None):
        """
        Create join group command

        :param cmd:     command info
        :param group:   group ID
        :return: JoinCommand object
        """
        super().__init__(cmd, GroupCommand.JOIN, group=group)


class QuitCommand(GroupCommand):

    def __init__(self, cmd: Optional[dict] = None, group: Optional[ID] = None):
        """
        Create member quit command

        :param cmd:     command info
        :param group:   group ID
        :return: QuitCommand object
        """
        super().__init__(cmd, GroupCommand.QUIT, group=group)


class QueryCommand(GroupCommand):

    def __init__(self, cmd: Optional[dict] = None, group: Optional[ID] = None):
        """
        Create query group members command (not history command)

        :param cmd:     command info
        :param group:   group ID
        :return: QueryCommand object
        """
        super().__init__(cmd, GroupCommand.QUERY, group=group)


class ResetCommand(GroupCommand):

    def __init__(self, cmd: Optional[dict] = None, group: Optional[ID] = None, members: Optional[List[ID]] = None):
        """
        Create reset group members command

        :param cmd:     command info
        :param group:   group ID
        :param members: member list
        :return: ResetCommand object
        """
        super().__init__(cmd, GroupCommand.RESET, group=group, members=members)
