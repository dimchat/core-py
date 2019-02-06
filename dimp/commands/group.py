# -*- coding: utf-8 -*-
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

from dkd.contents import serial_number

from mkm import ID
from dkd import MessageType, HistoryContent


class GroupCommand(HistoryContent):

    def __init__(self, content: dict):
        super().__init__(content)
        # group ID already fetched in Content.__init__
        # now fetch member ID
        if 'member' in content:
            self.member = ID(content['member'])
        else:
            self.member = None

    @classmethod
    def membership(cls, command: str, group: ID, member: ID=None, time: int=0) -> HistoryContent:
        content = {
            'type': MessageType.History,
            'sn': serial_number(),
            'command': command,
            'time': time,
            'group': group,
        }
        if member:
            content['member'] = member
        return GroupCommand(content)

    @classmethod
    def invite(cls, group: ID, member: ID, time: int=0) -> HistoryContent:
        """
        Create invite group member command

        :param group: Group ID
        :param member: Member ID
        :param time: Timestamp
        :return: GroupCommand object
        """
        return cls.membership(command='invite', group=group, member=member, time=time)

    @classmethod
    def expel(cls, group: ID, member: ID, time: int=0) -> HistoryContent:
        """
        Create expel group member command

        :param group: Group ID
        :param member: Member ID
        :param time: Timestamp
        :return: GroupCommand object
        """
        return cls.membership(command='expel', group=group, member=member, time=time)

    @classmethod
    def quit(cls, group: ID, time: int=0) -> HistoryContent:
        """
        Create member quit command

        :param group: Group ID
        :param time: Timestamp
        :return: GroupCommand object
        """
        return cls.membership(command='quit', group=group, time=time)
