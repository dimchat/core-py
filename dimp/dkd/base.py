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
from typing import Optional, Union, Any, Dict

from mkm.types import Dictionary
from dkd.factory import MessageFactoryManager
from dkd import ContentType, Content
from dkd import InstantMessage
from mkm import ID

from ..protocol import Command
from .factory import CommandFactoryManager


"""
    Message Content
    ~~~~~~~~~~~~~~~

    Base implementation of Content
"""


class BaseContent(Dictionary, Content):

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 msg_type: Union[int, ContentType] = 0):
        if content is None:
            if isinstance(msg_type, ContentType):
                msg_type = msg_type.value
            assert msg_type > 0, 'content type error: %d' % msg_type
            time = time_lib.time()
            sn = InstantMessage.generate_serial_number(msg_type=msg_type, time=time)
            content = {
                'type': msg_type,
                'sn': sn,
                'time': time,
            }
        else:
            sn = 0
            time = 0
        # initialize with content info
        super().__init__(dictionary=content)
        # lazy load
        self.__type = msg_type
        self.__sn = sn
        self.__time = time
        self.__group = None

    @property  # Override
    def type(self) -> int:
        """ message content type: text, image, ... """
        if self.__type == 0:
            gf = MessageFactoryManager.general_factory
            msg_type = gf.get_content_type(content=self.dictionary)
            if msg_type is None:
                msg_type = 0
            self.__type = msg_type
        return self.__type

    @property  # Override
    def sn(self) -> int:
        """ serial number: random number to identify message content """
        if self.__sn == 0:
            self.__sn = self.get_int(key='sn')
        return self.__sn

    @property  # Override
    def time(self) -> Optional[float]:
        if self.__time == 0:
            self.__time = self.get_time(key='time')
        return self.__time

    @property  # Override
    def group(self) -> Optional[ID]:
        if self.__group is None:
            identifier = self.get(key='group')
            self.__group = ID.parse(identifier=identifier)
        return self.__group

    @group.setter  # Override
    def group(self, identifier: ID):
        if identifier is None:
            self.pop('group', None)
        else:
            self['group'] = str(identifier)
        self.__group = identifier


"""
    Base Command
"""


class BaseCommand(BaseContent, Command):

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 msg_type: Union[int, ContentType] = 0,
                 cmd: Optional[str] = None):
        if content is None and msg_type == 0:
            msg_type = ContentType.COMMAND
        super().__init__(content=content, msg_type=msg_type)
        if cmd is not None:
            self['command'] = cmd

    @property  # Override
    def cmd(self) -> str:
        gf = CommandFactoryManager.general_factory
        name = gf.get_cmd(content=self.dictionary)
        return '' if name is None else name
