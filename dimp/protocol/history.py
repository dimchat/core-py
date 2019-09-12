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

from dkd import Content, ContentType
from dkd.content import message_content_classes


class HistoryCommand(Content):
    """
        Group History Command
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x89,
            sn   : 123,

            command : "...", // command name
            time    : 0,     // command timestamp
            extra   : info   // command parameters
        }
    """

    def __init__(self, content: dict):
        super().__init__(content)
        # value of 'command' & 'time' cannot be changed again
        self.__command = content['command']
        time = content.get('time')
        if time is None:
            self.__time = 0
        else:
            self.__time = int(time)

    @property
    def command(self) -> str:
        return self.__command

    @property
    def time(self) -> int:
        return self.__time

    #
    #   Factory
    #
    @classmethod
    def new(cls, command: str, time: int=0) -> Content:
        if time == 0:
            time = int(time_lib.time())
        content = {
            'type': ContentType.History,
            'time': time,
            'command': command,
        }
        return HistoryCommand(content)


message_content_classes[ContentType.History] = HistoryCommand
