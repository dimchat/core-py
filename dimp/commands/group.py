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

import time as time_lib

from mkm import ID
from dkd import ContentType

from ..protocol import HistoryCommand


class GroupCommand(HistoryCommand):
    """
        Group Command
        ~~~~~~~~~~~~~

        data format: {
            type : 0x89,
            sn   : 123,

            command : "invite",      // "expel", "quit"
            time    : 0,             // timestamp
            group   : "{GROUP_ID}",  // group ID
            member  : "{MEMBER_ID}", // member ID
        }
    """

    #
    #   group (group ID already fetched in Content.__init__)
    #

    #
    #   member
    #
    @property
    def member(self) -> ID:
        value = self.get('member')
        if value:
            return ID(value)

    @member.setter
    def member(self, value: str):
        if value is None:
            self.pop('member', None)
        else:
            self['member'] = value

    @property
    def members(self) -> list:
        value = self.get('members')
        if value:
            # TODO: convert all items to ID objects
            return value

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
    def membership(cls, command: str, group: str, member: str=None, members: list=None, time: int=0) -> HistoryCommand:
        if time == 0:
            time = int(time_lib.time())
        content = {
            'type': ContentType.History,
            'command': command,
            'time': time,
            'group': group,
        }
        if members is not None:
            content['members'] = members
        elif member is not None:
            content['member'] = member
        return GroupCommand(content)

    @classmethod
    def invite(cls, group: str, member: str=None, members: list=None, time: int=0) -> HistoryCommand:
        """
        Create invite group member command

        :param group: Group ID
        :param member: Member ID
        :param members: Member list
        :param time: Timestamp
        :return: GroupCommand object
        """
        return cls.membership(command='invite', group=group, member=member, members=members, time=time)

    @classmethod
    def expel(cls, group: str, member: str=None, members: list=None, time: int=0) -> HistoryCommand:
        """
        Create expel group member command

        :param group: Group ID
        :param member: Member ID
        :param members: Member list
        :param time: Timestamp
        :return: GroupCommand object
        """
        return cls.membership(command='expel', group=group, member=member, members=members, time=time)

    @classmethod
    def quit(cls, group: str, time: int=0) -> HistoryCommand:
        """
        Create member quit command

        :param group: Group ID
        :param time: Timestamp
        :return: GroupCommand object
        """
        return cls.membership(command='quit', group=group, time=time)

    @classmethod
    def query(cls, group: str, time: int=0) -> HistoryCommand:
        """
        Create query group members command

        :param group: Group ID
        :param time: Timestamp
        :return: GroupCommand object
        """
        return cls.membership(command='query', group=group, time=time)

    @classmethod
    def reset(cls, group: str, members: list, time: int=0) -> HistoryCommand:
        """
        Create reset group members command

        :param group: Group ID
        :param members: Member list
        :param time: Timestamp
        :return: GroupCommand object
        """
        return cls.membership(command='reset', group=group, members=members, time=time)
