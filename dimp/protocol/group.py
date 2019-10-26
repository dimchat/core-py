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

from .command import command_classes
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

    def __new__(cls, cmd: dict):
        """
        Create group command

        :param cmd: group command info
        :return: GroupCommand object
        """
        if cmd is None:
            return None
        elif cls is GroupCommand:
            if isinstance(cmd, GroupCommand):
                # return GroupCommand object directly
                return cmd
            # get class by command name
            clazz = command_classes.get(cmd['command'])
            if clazz is not None:
                assert issubclass(clazz, GroupCommand), '%s must be sub-class of GroupCommand' % clazz
                return clazz(cmd)
        # subclass or default GroupCommand(dict)
        return super().__new__(cls, cmd)

    #
    #   group (group ID already fetched in Content.__init__)
    #

    #
    #   member/members
    #
    @property
    def member(self) -> str:
        # TODO: convert value to ID object
        return self.get('member')

    @member.setter
    def member(self, value: str):
        if value is None:
            self.pop('member', None)
        else:
            self['member'] = value

    @property
    def members(self) -> list:
        # TODO: convert all items to ID objects
        return self.get('members')

    @members.setter
    def members(self, value: list):
        if value is None:
            self.pop('members', None)
        else:
            self['members'] = value

    #
    #   Factories
    #
    @classmethod
    def __new(cls, command: str, group: str, member: str=None, members: list=None, time: int=0):
        content = {
            'command': command,
            'group': group,
        }
        if members is not None:
            content['members'] = members
        elif member is not None:
            content['member'] = member
        if time > 0:
            content['time'] = time
        return HistoryCommand.new(content)

    @classmethod
    def invite(cls, group: str, member: str=None, members: list=None, time: int=0):
        """
        Create invite group member command

        :param group:   Group ID
        :param member:  Member ID
        :param members: Member list
        :param time:    Timestamp
        :return: GroupCommand object
        """
        return cls.__new(command=HistoryCommand.INVITE, group=group, member=member, members=members, time=time)

    @classmethod
    def expel(cls, group: str, member: str=None, members: list=None, time: int=0):
        """
        Create expel group member command

        :param group:   Group ID
        :param member:  Member ID
        :param members: Member list
        :param time:    Timestamp
        :return: GroupCommand object
        """
        return cls.__new(command=HistoryCommand.EXPEL, group=group, member=member, members=members, time=time)

    @classmethod
    def quit(cls, group: str, time: int=0):
        """
        Create member quit command

        :param group: Group ID
        :param time:  Timestamp
        :return: GroupCommand object
        """
        return cls.__new(command=HistoryCommand.QUIT, group=group, time=time)

    @classmethod
    def query(cls, group: str, time: int=0):
        """
        Create query group members command

        :param group: Group ID
        :param time:  Timestamp
        :return: GroupCommand object
        """
        return cls.__new(command=HistoryCommand.QUERY, group=group, time=time)

    @classmethod
    def reset(cls, group: str, members: list, time: int=0):
        """
        Create reset group members command

        :param group:   Group ID
        :param members: Member list
        :param time:    Timestamp
        :return: GroupCommand object
        """
        return cls.__new(command=HistoryCommand.RESET, group=group, members=members, time=time)


class InviteCommand(GroupCommand):

    def __new__(cls, cmd: dict):
        """
        Create invite group command

        :param cmd: group command info
        :return: InviteCommand object
        """
        if cmd is None:
            return None
        elif cls is InviteCommand:
            if isinstance(cmd, InviteCommand):
                # return InviteCommand object directly
                return cmd
        # new InviteCommand(dict)
        return super().__new__(cls, cmd)


class ExpelCommand(GroupCommand):

    def __new__(cls, cmd: dict):
        """
        Create expel group command

        :param cmd: group command info
        :return: ExpelCommand object
        """
        if cmd is None:
            return None
        elif cls is ExpelCommand:
            if isinstance(cmd, ExpelCommand):
                # return ExpelCommand object directly
                return cmd
        # new ExpelCommand(dict)
        return super().__new__(cls, cmd)


class JoinCommand(GroupCommand):

    def __new__(cls, cmd: dict):
        """
        Create join group command

        :param cmd: group command info
        :return: JoinCommand object
        """
        if cmd is None:
            return None
        elif cls is JoinCommand:
            if isinstance(cmd, JoinCommand):
                # return JoinCommand object directly
                return cmd
        # new JoinCommand(dict)
        return super().__new__(cls, cmd)


class QuitCommand(GroupCommand):

    def __new__(cls, cmd: dict):
        """
        Create quit group command

        :param cmd: group command info
        :return: QuitCommand object
        """
        if cmd is None:
            return None
        elif cls is QuitCommand:
            if isinstance(cmd, QuitCommand):
                # return QuitCommand object directly
                return cmd
        # new QuitCommand(dict)
        return super().__new__(cls, cmd)


class QueryCommand(GroupCommand):

    def __new__(cls, cmd: dict):
        """
        Create query group command

        :param cmd: group command info
        :return: QueryCommand object
        """
        if cmd is None:
            return None
        elif cls is QueryCommand:
            if isinstance(cmd, QueryCommand):
                # return QueryCommand object directly
                return cmd
        # new QueryCommand(dict)
        return super().__new__(cls, cmd)


class ResetCommand(GroupCommand):

    def __new__(cls, cmd: dict):
        """
        Create reset group command

        :param cmd: group command info
        :return: ResetCommand object
        """
        if cmd is None:
            return None
        elif cls is ResetCommand:
            if isinstance(cmd, ResetCommand):
                # return ResetCommand object directly
                return cmd
        # new ResetCommand(dict)
        return super().__new__(cls, cmd)


# register group command classes
command_classes[HistoryCommand.INVITE] = InviteCommand
command_classes[HistoryCommand.EXPEL] = ExpelCommand
command_classes[HistoryCommand.JOIN] = JoinCommand
command_classes[HistoryCommand.QUIT] = QuitCommand
command_classes[HistoryCommand.QUERY] = QueryCommand
command_classes[HistoryCommand.RESET] = ResetCommand
