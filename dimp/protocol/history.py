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

from dkd import ContentType

from .content import Content
from .command import Command

import dimp  # dimp.GroupCommand


class HistoryCommand(Command):
    """
        History Command
        ~~~~~~~~~~~~~~~

        data format: {
            type : 0x89,
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

    # group: founder/owner
    FOUND = "found"
    ABDICATE = "abdicate"
    # group: member
    INVITE = "invite"
    EXPEL = "expel"
    JOIN = "join"
    QUIT = "quit"
    RESET = "reset"
    QUERY = "query"  # (not history command)
    # group: administrator/assistant
    HIRE = "hire"
    FIRE = "fire"
    RESIGN = "resign"
    # -------- command names end --------

    def __new__(cls, cmd: dict):
        """
        Create history command

        :param cmd: history info
        :return: HistoryCommand object
        """
        if cmd is None:
            return None
        elif cls is HistoryCommand:
            # check group
            if 'group' in cmd:
                # it's a group command
                # noinspection PyTypeChecker
                return dimp.GroupCommand.__new__(dimp.GroupCommand, cmd)
            if isinstance(cmd, HistoryCommand):
                # return HistoryCommand object directly
                return cmd
            # get class by command name
            clazz = cls.command_class(command=cmd['command'])
            if clazz is not None:
                # noinspection PyTypeChecker
                return clazz.__new__(clazz, cmd)
        # subclass or default HistoryCommand(dict)
        return super().__new__(cls, cmd)
    
    def __init__(self, content: dict):
        if self is content:
            # no need to init again
            return
        super().__init__(content)

    #
    #   Factory
    #
    @classmethod
    def new(cls, content: dict=None, command: str=None, time: int=0):
        """
        Create history command message content with 'command' as name

        :param content: command info
        :param command: command name
        :param time: command time
        :return: HistoryCommand object
        """
        if content is None:
            # create empty content
            content = {}
        # set content type: 'History'
        if 'type' not in content:
            content['type'] = ContentType.History
        # new HistoryCommand(dict)
        return super().new(content, command=command, time=time)


# register content class with type
Content.register(content_type=ContentType.History, content_class=HistoryCommand)
