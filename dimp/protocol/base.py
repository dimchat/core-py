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

from abc import ABC, abstractmethod
from typing import Optional, Any, Dict

from mkm.types import Singleton
from mkm.types import DateTime
from mkm.types import Dictionary
from mkm import ID
from dkd import Content
from dkd import InstantMessage
from dkd.plugins import SharedMessageExtensions

from .helpers import CommandExtensions
from .types import ContentType


class Command(Content, ABC):
    """
        Command Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x88),
            sn   : 123,

            command : "...", // command name
            extra   : info   // command parameters
        }
    """

    # -------- command names begin --------
    META = 'meta'
    DOCUMENTS = 'documents'
    RECEIPT = 'receipt'
    # -------- command names end --------

    @property
    @abstractmethod
    def cmd(self) -> str:
        """ command/method/declaration """
        raise NotImplemented

    #
    #   Factory method
    #

    @classmethod
    def parse(cls, content: Any):  # -> Optional[Command]:
        helper = cmd_helper()
        return helper.parse_command(content=content)

    @classmethod
    def get_factory(cls, cmd: str):  # -> Optional[CommandFactory]:
        helper = cmd_helper()
        return helper.get_command_factory(cmd=cmd)

    @classmethod
    def set_factory(cls, cmd: str, factory):
        helper = cmd_helper()
        helper.set_command_factory(cmd=cmd, factory=factory)


def cmd_helper():
    helper = CommandExtensions.cmd_helper
    assert isinstance(helper, CommandHelper), 'command helper error: %s' % helper
    return helper


class CommandFactory(ABC):
    """ Command Factory """

    @abstractmethod
    def parse_command(self, content: Dict) -> Optional[Command]:
        """
        Parse map object to command

        :param content: command content
        :return: Command
        """
        raise NotImplemented


########################
#                      #
#   Plugins: Helpers   #
#                      #
########################


class CommandHelper(ABC):
    """ General Helper """

    @abstractmethod
    def set_command_factory(self, cmd: str, factory: CommandFactory):
        raise NotImplemented

    @abstractmethod
    def get_command_factory(self, cmd: str) -> Optional[CommandFactory]:
        raise NotImplemented

    @abstractmethod
    def parse_command(self, content: Any) -> Optional[Command]:
        raise NotImplemented


# class GeneralCommandHelper(CommandHelper, ABC):
class GeneralCommandHelper(ABC):
    """ Command GeneralFactory """

    #
    #   CMD - Command, Method, Declaration
    #

    @abstractmethod
    def get_cmd(self, content: Dict, default: Optional[str] = None) -> Optional[str]:
        raise NotImplemented


@Singleton
class SharedCommandExtensions:
    """ Command FactoryManager """

    def __init__(self):
        super().__init__()
        self.__helper: Optional[GeneralCommandHelper] = None

    @property
    def helper(self) -> Optional[GeneralCommandHelper]:
        return self.__helper

    @helper.setter
    def helper(self, helper: GeneralCommandHelper):
        self.__helper = helper

    #
    #   Command
    #

    @property
    def cmd_helper(self) -> Optional[CommandHelper]:
        return CommandExtensions.cmd_helper

    @cmd_helper.setter
    def cmd_helper(self, helper: CommandHelper):
        CommandExtensions.cmd_helper = helper


###############################
#                             #
#   DaoKeDao Implementation   #
#                             #
###############################


class BaseContent(Dictionary, Content):

    def __init__(self, content: Dict = None, msg_type: str = None):
        # check parameters
        if content is None:
            # 1. new content with type
            assert msg_type is not None and len(msg_type) > 0, 'content type error: %s' % msg_type
            time = DateTime.now()
            sn = InstantMessage.generate_serial_number(msg_type, time)
            content = {
                'type': msg_type,
                'sn': sn,
                'time': time.timestamp,
            }
        else:
            # 2. content info from network
            assert msg_type is None, 'params error: %s, %s' % (content, msg_type)
            # lazy load
            sn = None
            time = None
        # initialize with content info
        super().__init__(dictionary=content)
        self.__type = msg_type
        self.__sn = sn
        self.__time = time

    @property  # Override
    def type(self) -> str:
        """ message content type: text, image, ... """
        if self.__type is None:
            ext = SharedMessageExtensions()
            self.__type = ext.helper.get_content_type(content=self.dictionary, default='')
            # self.__type = self.get_int(key='type', default=0)
        return self.__type

    @property  # Override
    def sn(self) -> int:
        """ serial number: random number to identify message content """
        if self.__sn is None:
            self.__sn = self.get_int(key='sn', default=0)
        return self.__sn

    @property  # Override
    def time(self) -> Optional[DateTime]:
        if self.__time is None:
            self.__time = self.get_datetime(key='time', default=None)
        return self.__time

    @property  # Override
    def group(self) -> Optional[ID]:
        return ID.parse(identifier=self.get('group'))

    @group.setter  # Override
    def group(self, identifier: ID):
        self.set_string(key='group', value=identifier)


class BaseCommand(BaseContent, Command):

    def __init__(self, content: Dict = None, msg_type: str = None, cmd: str = None):
        # check parameters
        if content is None:
            # 1. new command with type & name
            if msg_type is None:
                msg_type = ContentType.COMMAND
            assert cmd is not None and len(cmd) > 0, 'command name should not empty'
            super().__init__(None, msg_type)
            self['command'] = cmd
        else:
            # 2. command info from network
            assert msg_type is None and cmd is None, 'params error: %s, %s' % (msg_type, cmd)
            super().__init__(content)

    @property  # Override
    def cmd(self) -> str:
        ext = SharedCommandExtensions()
        return ext.helper.get_cmd(content=self.dictionary, default='')
        # return self.get_str(key='command', default='')
