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

from mkm.types import DateTime
from mkm import ID

from ..protocol import ContentType
from ..protocol import HistoryCommand, GroupCommand
from ..protocol import InviteCommand, ExpelCommand, JoinCommand, QuitCommand, QueryCommand, ResetCommand

from .base import BaseCommand


class BaseHistoryCommand(BaseCommand, HistoryCommand):
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

    def __init__(self, content: Dict[str, Any] = None,
                 msg_type: str = None, cmd: str = None):
        if content is None:
            if msg_type is None:
                msg_type = ContentType.HISTORY
            assert cmd is not None, 'command name should not empty'
        super().__init__(content, msg_type, cmd=cmd)


class BaseGroupCommand(BaseHistoryCommand, GroupCommand):
    """
        Group Command
        ~~~~~~~~~~~~~

        data format: {
            type : i2s(0x89),
            sn   : 123,

            command : "invite",         // "expel", "quit"
            time    : 0,                // timestamp
            group   : "{GROUP_ID}",     // group ID
            member  : "{MEMBER_ID}",    // member ID
            members : ["{MEMBER_ID}",], // member ID list
        }
    """

    def __init__(self, content: Dict[str, Any] = None,
                 cmd: str = None, group: ID = None,
                 member: ID = None, members: List[ID] = None):
        super().__init__(content, None, cmd=cmd)
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
    def member(self, user: ID):
        self.set_string(key='member', value=user)
        self.pop('members', None)

    @property  # Override
    def members(self) -> Optional[List[ID]]:
        array = self.get('members')
        if array is not None:
            # convert all items to ID objects
            return ID.convert(array=array)
        # get from 'member'
        single = self.member
        return [] if single is None else [single]

    @members.setter  # Override
    def members(self, users: List[ID]):
        if users is None:
            self.pop('members', None)
        else:
            self['members'] = ID.revert(identifiers=users)
        self.pop('member', None)


class InviteGroupCommand(BaseGroupCommand, InviteCommand):

    def __init__(self, content: Dict[str, Any] = None,
                 group: ID = None, member: ID = None, members: List[ID] = None):
        """
        Create invite group member command

        :param content: command content
        :param group:   group ID
        :param member:  member ID
        :param members: member list
        :return: InviteCommand object
        """
        cmd = GroupCommand.INVITE if content is None else None
        super().__init__(content, cmd=cmd, group=group, member=member, members=members)


class ExpelGroupCommand(BaseGroupCommand, ExpelCommand):
    """ Deprecated, use 'reset' instead """

    def __init__(self, content: Dict[str, Any] = None,
                 group: ID = None, member: ID = None, members: List[ID] = None):
        """
        Create expel group member command

        :param content: command content
        :param group:   group ID
        :param member:  member ID
        :param members: member list
        :return: ExpelCommand object
        """
        cmd = GroupCommand.EXPEL if content is None else None
        super().__init__(content, cmd=cmd, group=group, member=member, members=members)


class JoinGroupCommand(BaseGroupCommand, JoinCommand):

    def __init__(self, content: Dict[str, Any] = None, group: ID = None):
        """
        Create join group command

        :param content: command content
        :param group:   group ID
        :return: JoinCommand object
        """
        cmd = GroupCommand.JOIN if content is None else None
        super().__init__(content, cmd=cmd, group=group)


class QuitGroupCommand(BaseGroupCommand, QuitCommand):

    def __init__(self, content: Dict[str, Any] = None, group: ID = None):
        """
        Create member quit command

        :param content: command content
        :param group:   group ID
        :return: QuitCommand object
        """
        cmd = GroupCommand.QUIT if content is None else None
        super().__init__(content, cmd=cmd, group=group)


class QueryGroupCommand(BaseGroupCommand, QueryCommand):

    def __init__(self, content: Dict[str, Any] = None, group: ID = None, last_time: DateTime = None):
        """
        Create query group members command (not history command)

        :param content: command content
        :param group:   group ID
        :return: QueryCommand object
        """
        cmd = GroupCommand.QUERY if content is None else None
        super().__init__(content, cmd=cmd, group=group)
        if last_time is not None:
            self.set_datetime(key='last_time', value=last_time)

    @property  # Override
    def last_time(self) -> Optional[DateTime]:
        return self.get_datetime(key='last_time', default=None)


class ResetGroupCommand(BaseGroupCommand, ResetCommand):

    def __init__(self, content: Dict[str, Any] = None, group: ID = None, members: List[ID] = None):
        """
        Create reset group members command

        :param content: command content
        :param group:   group ID
        :param members: member list
        :return: ResetCommand object
        """
        cmd = GroupCommand.RESET if content is None else None
        super().__init__(content, cmd=cmd, group=group, members=members)
