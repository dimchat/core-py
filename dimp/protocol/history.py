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

import time as time_lib
from typing import Union

from dkd import ContentType
from dkd.content import message_content_classes

from .command import Command


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
    QUERY = "query"
    RESET = "reset"
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
        elif isinstance(cmd, HistoryCommand):
            # return HistoryCommand object directly
            return cmd
        elif cls is HistoryCommand:
            # check group
            if 'group' in cmd:
                # it's a group command
                from .group import GroupCommand
                return GroupCommand(cmd)
        # new HistoryCommand(dict)
        return super().__new__(cls, cmd)
    
    def __init__(self, content: dict):
        super().__init__(content)
        # value of 'time' cannot be changed again
        time = content.get('time')
        if time is None:
            self.__time = 0
        else:
            self.__time = int(time)

    @property
    def time(self) -> int:
        return self.__time

    #
    #   Factory
    #
    @classmethod
    def new(cls, command: Union[str, dict]):
        if isinstance(command, str):
            content = {
                'type': ContentType.History,
                'command': command,
                'time': int(time_lib.time()),
            }
        elif isinstance(command, dict):
            content = command
            if 'type' not in content:
                content['type'] = ContentType.History
            if 'time' not in content:
                content['time'] = int(time_lib.time())
            assert 'command' in content, 'command error: %s' % command
        else:
            raise TypeError('history argument error: %s' % command)
        # new HistoryCommand(dict)
        return Command.new(content)


# register content class
message_content_classes[ContentType.History] = HistoryCommand
